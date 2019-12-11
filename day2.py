#!/usr/bin/env python3
import logging
import fileinput
from itertools import product
from collections import defaultdict
import operator
import sys


def op_sum(program, pos, pmodes):
  return op_bin(program, pos, pmodes, operator.add)

def op_mul(program, pos, pmodes):
  return op_bin(program, pos, pmodes, operator.mul)

def op_bin(program, pos, pmodes, operation):
  arr = program.code
  
  if pmodes[0] == 0:
    first_operand_location = arr[pos+1]
  elif pmodes[0] == 1:
    first_operand_location = pos+1
  else:
    first_operand_location = arr[pos+1] + program.relative_base 

  first_operand = arr[first_operand_location]

  if pmodes[1] == 0:
    second_operand_location = arr[pos+2]
  elif pmodes[1] == 1:
    second_operand_location = pos+2
  else:
    second_operand_location = arr[pos+2] +program.relative_base

  second_operand = arr[second_operand_location]

  logging.debug(f"{operation=} {first_operand=} {second_operand=}")
  op_result = operation(first_operand, second_operand)

  if pmodes[2] == 0:
    result_location = arr[pos+3]
  elif pmodes[2] == 2:
    result_location = arr[pos+3] + program.relative_base
  else:
    logging.error(f"Write location parameter in immediate mode")
    return (0, None)

  logging.debug(f"{result_location=} {op_result=}")
  arr[result_location] = op_result

  return (1, None)


def op_inp(program, pos, pmodes):
  arr = program.code
  logging.info("INP:")
  try:
    inp = int(input())
  except EOFError:
    logging.info("Suspended")
    return (0, None)

  if pmodes[0] == 0:
    dest = arr[pos+1]
  elif pmodes[0] == 2:
    dest = arr[pos+1] + program.relative_base
  else:
    logging.error(f"Write location parameter in immediate mode")
    return (0, None)

  arr[dest] = inp
  logging.debug(f"Read {inp=}")

  return (1, None)


def op_out(program, pos, pmodes):
  arr = program.code
  if pmodes[0] == 0:
    out_loc = arr[pos+1]
  elif pmodes[0] == 1:
    out_loc = pos+1
  else:
    out_loc = arr[pos+1]+program.relative_base
  
  out = arr[out_loc]

  outmsg = f"{out}\n"
  if not sys.stdout.isatty():
    sys.stdout.write(outmsg)
    sys.stdout.seek(sys.stdout.tell() - len(outmsg))
  logging.info(f"OUT: {outmsg}")

  return (1, None)


def op_halt(program,pos, pmodes):
  arr = program.code
  logging.info("HALT")
  return (0, None)

def _op_jmp_cnd(program, pos, pmodes, cnd):
  arr = program.code
  logging.debug("Jmp cnd:")
  new_pc = None
  if pmodes[0] == 0:
    flag_loc = arr[pos+1]
  elif pmodes[0] == 1:
    flag_loc = pos+1
  else:
    flag_loc = arr[pos+1] + program.relative_base
    
  flag = arr[flag_loc]
  logging.debug(f"{flag=}")

  if cnd(flag):
    if pmodes[1] == 0:
      new_pc_loc = arr[pos+2]
      new_pc = arr[new_pc_loc]
    elif pmodes[1] == 1:
      new_pc = arr[pos+2]
    else:
      new_pc_loc = arr[pos+2] + program.relative_base
      new_pc = arr[new_pc_loc]

  return (1, new_pc)

def op_jnz(program, pos, pmodes):
  return _op_jmp_cnd(program, pos, pmodes, lambda x: x != 0)


def op_jz(program, pos, pmodes):
  return _op_jmp_cnd(program, pos, pmodes, lambda x: x == 0)


def op_lt(program, pos, pmodes):
  return op_bin(program, pos, pmodes, lambda a,b: 1 if a < b else 0)


def op_eq(program, pos, pmodes):
  return op_bin(program, pos, pmodes, lambda a,b: 1 if a == b else 0)

def op_rel(program, pos, pmodes):
  arr = program.code
  if pmodes[0] == 0:
    program.relative_base += arr[arr[pos+1]]
  elif pmodes[0] == 1:
    program.relative_base += arr[pos+1]
  else:
    program.relative_base += arr[arr[pos + 1] + program.relative_base]

  logging.debug(f"Set {program.relative_base=}")
  return (1, None)

OPERATIONS = {
         # Opcode: (function, num_params)
                1: (op_sum, 3),
                2: (op_mul, 3),
                3: (op_inp, 1),
                4: (op_out, 1),
                5: (op_jnz, 2),
                6: (op_jz,  2),
                7: (op_lt,  3),
                8: (op_eq,  3),
                9: (op_rel, 1),
               99: (op_halt, 0)}

def read_instruction(instruction):
  opcode = None
  parameter_modes = [] 
  opcode = instruction % 100
  power = 3
  while instruction // pow(10,power-1):
    param_mode = ((instruction % pow(10,power)) - (instruction % pow(10,power -1))) // pow(10, power-1)
    parameter_modes.append(param_mode)
    power+=1

  num_params = OPERATIONS[opcode][1]
  # fill all missing params with zeroes, as that is default mode
  parameter_modes.extend( [0] * (num_params - len(parameter_modes)))

  logging.debug(f"instruction {opcode=}")
  logging.debug(f"{parameter_modes=}")
  return (opcode, parameter_modes)


class Program(object):
  def __init__(self, code, pc, rb):
    self.code = code
    self.pc = pc 
    self.relative_base = rb


def intcode(code, pc = 0, relative_base=0):
  logging.info(f"Input code: {code}")
  logging.info(f"Program counter: {pc}")

  program = Program(code, pc, relative_base)

  while True:
    instruction = program.code[program.pc]
    logging.debug(f"Processing {instruction=}")
    (opcode, param_modes) = read_instruction(instruction)
    try:
      logging.debug(f"Processing {opcode=}")
      (operation, num_params) = OPERATIONS[opcode]
      (result, new_pc) = operation(program, program.pc, param_modes)
    except KeyError:
      logging.error(f"Invalid operation: {opcode=}")
      return
    if result:
      if new_pc is not None:
        program.pc = new_pc
      else:
        # +1 to move from instruction loc
        program.pc += (num_params+1)
      logging.debug(f"{program.pc=}")
    else:
      break

  #logging.info(f"Processed program: {','.join(map(str,program.code))}")
  #return code[0]
  return program.pc
    
def operate(memory, noun, verb):
  opcodes = memory[:]
  opcodes[1] = noun
  opcodes[2] = verb
  result = intcode(opcodes)
  logging.info(f"{result=}")
  return result

def find_result(target, code):
  possible_inputs = product(range(100), repeat=2)
  for noun, verb in possible_inputs:
    result = operate(code, noun, verb)
    if result == target:
      logging.info(f"{target=} reached with {noun=},{verb=}")
      logging.info(f"Answer: {100*noun+verb}")
      return (noun,verb)
   
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO) 
  for line in fileinput.input():
    #oldcode = list(map(int,line.split(','))) 
    code = defaultdict(int)
    data = (map(int,line.split(',')))
    for i, instruction in enumerate(data):
      code[i] = instruction
    #operate(code, 12, 2)
    #find_result(19690720, code)
    intcode(code)
