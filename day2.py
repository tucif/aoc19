#!/usr/bin/env python3
import logging
import fileinput
from itertools import product
from collections import defaultdict
from io import StringIO
import operator
import sys

RET_STOP = 0
RET_CONT = 1
RET_NEWPC = 2

def op_sum(program, pmodes):
  return op_bin(program, pmodes, operator.add)

def op_mul(program, pmodes):
  return op_bin(program, pmodes, operator.mul)

def op_bin(program, pmodes, operation):
  arr = program.code
  pos = program.pc
  
  if pmodes[0] == 0:
    first_operand_location = arr[pos+1]
  elif pmodes[0] == 1:
    first_operand_location = pos+1
  else:
    first_operand_location = arr[pos+1] + program.relative_base 

  logging.debug(f"{first_operand_location=}")
  first_operand = arr[first_operand_location]

  if pmodes[1] == 0:
    second_operand_location = arr[pos+2]
  elif pmodes[1] == 1:
    second_operand_location = pos+2
  else:
    second_operand_location = arr[pos+2] +program.relative_base

  logging.debug(f"{second_operand_location=}")
  second_operand = arr[second_operand_location]

  logging.debug(f"{operation=} {first_operand=} {second_operand=}")
  op_result = operation(first_operand, second_operand)

  if pmodes[2] == 0:
    result_location = arr[pos+3]
  elif pmodes[2] == 2:
    result_location = arr[pos+3] + program.relative_base
  else:
    logging.error(f"Write location parameter in immediate mode")
    return RET_STOP

  logging.debug(f"{result_location=} {op_result=}")
  arr[result_location] = op_result

  return RET_CONT


def op_inp(program, pmodes):
  arr = program.code
  pos = program.pc
  logging.info("INP:")
  try:
    inp = int(input())
  except EOFError:
    logging.info("Suspended")
    return RET_STOP

  if pmodes[0] == 0:
    dest = arr[pos+1]
  elif pmodes[0] == 2:
    dest = arr[pos+1] + program.relative_base
  else:
    logging.error(f"Write location parameter in immediate mode")
    return RET_STOP

  arr[dest] = inp
  logging.info(f"Read {inp=}")
  logging.debug(f"Stored into {dest=}")

  return RET_CONT


def op_out(program, pmodes):
  arr = program.code
  pos = program.pc
  output = program.output
  if pmodes[0] == 0:
    out_loc = arr[pos+1]
  elif pmodes[0] == 1:
    out_loc = pos+1
  else:
    out_loc = arr[pos+1]+program.relative_base
  
  out = arr[out_loc]
  logging.debug(f"{out_loc=}")

  outmsg = f"{out}\n"
  if output:
    output.write(outmsg)
    if program.rewind_output:
      output.seek(output.tell() - len(outmsg))
  logging.info(f"OUT: {out}")

  return RET_CONT


def op_halt(program, pmodes):
  arr = program.code
  logging.info("HALT")
  return RET_STOP

def _op_jmp_cnd(program, pmodes, cnd):
  arr = program.code
  pos = program.pc
  logging.debug(f"Jmp {cnd=}")
  new_pc = None
  if pmodes[0] == 0:
    flag_loc = arr[pos+1]
  elif pmodes[0] == 1:
    flag_loc = pos+1
  else:
    flag_loc = arr[pos+1] + program.relative_base
    
  logging.debug(f"{flag_loc=}")
  flag = arr[flag_loc]
  logging.debug(f"{flag=}")

  if cnd(flag):
    if pmodes[1] == 0:
      new_pc_loc = arr[pos+2]
    elif pmodes[1] == 1:
      new_pc_loc = pos+2
    else:
      new_pc_loc = arr[pos+2] + program.relative_base
    logging.debug(f"{new_pc_loc=}")
    new_pc = arr[new_pc_loc]
    program.pc = new_pc
    logging.debug(f"Jumped PC to {new_pc=}")
    return RET_NEWPC

  return RET_CONT

def op_jnz(program, pmodes):
  return _op_jmp_cnd(program, pmodes, lambda x: x != 0)


def op_jz(program, pmodes):
  return _op_jmp_cnd(program, pmodes, lambda x: x == 0)


def op_lt(program, pmodes):
  return op_bin(program, pmodes, lambda a,b: 1 if a < b else 0)


def op_eq(program, pmodes):
  return op_bin(program, pmodes, lambda a,b: 1 if a == b else 0)

def op_rel(program, pmodes):
  arr = program.code
  pos = program.pc
  if pmodes[0] == 0:
    rel_loc = arr[pos+1]
  elif pmodes[0] == 1:
    rel_loc = pos+1
  else:
    rel_loc = arr[pos+1] + program.relative_base

  logging.debug(f"{rel_loc=} {arr[rel_loc]=}")
  program.relative_base += arr[rel_loc]

  logging.debug(f"Set {program.relative_base=}")
  return RET_CONT

OPERATIONS = {
         # Opcode: (function, num_params)
                1: (op_sum, 3, "SUM"),
                2: (op_mul, 3, "MUL"),
                3: (op_inp, 1, "INP"),
                4: (op_out, 1, "OUT"),
                5: (op_jnz, 2, "JNZ"),
                6: (op_jz,  2, "JZ"),
                7: (op_lt,  3, "LT"),
                8: (op_eq,  3, "EQ"),
                9: (op_rel, 1, "REL"),
               99: (op_halt, 0, "HALT")}

def read_instruction(instruction):
  opcode = None
  parameter_modes = [] 
  opcode = instruction % 100
  power = 3
  logging.debug(f"Processing {instruction=}")
  while instruction // pow(10,power-1):
    param_mode = ((instruction % pow(10,power)) - (instruction % pow(10,power -1))) // pow(10, power-1)
    parameter_modes.append(param_mode)
    power+=1

  (op, num_params, opname) = OPERATIONS[opcode]
  # fill all missing params with zeroes, as that is default mode
  parameter_modes.extend( [0] * (num_params - len(parameter_modes)))

  logging.debug(f"instruction {opcode=} ({opname}) [{num_params} params]")
  logging.debug(f"{parameter_modes=}")
  return (opcode, parameter_modes)


class Program(object):
  def __init__(self, code, pc=0, rb=0, rw=1, output=None):
    self.code = self.init_program(code)
    self.pc = pc 
    self.relative_base = rb
    self.rewind_output = rw
    if output is None:
      self.output = sys.stdout
    else:
      self.output = output

  def init_program(self, codestring):
    if isinstance(codestring, str):
      code = defaultdict(int)
      data = (map(int,codestring.split(',')))
      for i, instruction in enumerate(data):
        code[i] = instruction
      return code
    else:
      return codestring

  def exec_standalone(self, initial_input):
    old_stdin = sys.stdin
    if initial_input:
      sys.stdin = StringIO(f"{initial_input}\n")

    result = intcode(self)

    #rewind the override
    self.output.seek(0)

    sys.stdin = old_stdin
    return result
  

def intcode(program):
  #logging.debug(f"Input code: {program.code}")

  while True:
    logging.debug(f"Program counter: {program.pc}")
    instruction = program.code[program.pc]
    (opcode, param_modes) = read_instruction(instruction)
    try:
      (operation, num_params, opname) = OPERATIONS[opcode]
      result = operation(program, param_modes)
    except KeyError:
      logging.error(f"Invalid operation: {opcode=}")
      return
    if result == RET_CONT:
      program.pc += (num_params+1)
      logging.debug(f"Updating pc by {num_params+1}")
    elif result == RET_STOP:
      break

  return program


def standalone(program, initial_input, stdout_override):
  program.output = stdout_override
  return program.exec_standalone(initial_input)
  
    
def operate(memory, noun, verb):
  opcodes = memory.copy()
  opcodes[1] = noun
  opcodes[2] = verb
  program = Program(opcodes)
  intcode(program)
  result = opcodes[0]
  logging.info(f"{result=}")
  return result


def find_result(target, code):
  possible_inputs = product(range(100), repeat=2)
  for noun, verb in possible_inputs:
    result = operate(code, noun, verb)
    if result == target:
      logging.info(f"{target=} reached with {noun=},{verb=}")
      logging.info(f"Answer: {100*noun+verb}")
      return 100*noun+verb
   

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO) 
  for line in fileinput.input():
    #operate(code, 12, 2)
    #find_result(19690720, code)
    program = Program(line)
    intcode(program)
