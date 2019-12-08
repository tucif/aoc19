#!/usr/bin/env python3
import logging
import fileinput
from itertools import product

def op_sum(arr, pos, pmodes):
  op_bin(arr, pos, lambda a,b: a+b, pmodes)
  return 1

def op_mul(arr,pos,pmodes):
  op_bin(arr, pos, lambda a,b: a*b, pmodes)
  return 1

def op_bin(arr, pos, operation, pmodes):
  
  if pmodes[0] == 0:
    first_operand_location = arr[pos+1]
    first_operand = arr[first_operand_location]
  else:
    first_operand = arr[pos+1]

  if pmodes[1] == 0:
    second_operand_location = arr[pos+2]
    second_operand = arr[second_operand_location]
  else:
    second_operand = arr[pos+2]

  logging.debug(f"{operation=} {first_operand=} {second_operand=}")
  op_result = operation(first_operand, second_operand)

  if pmodes[2] == 0:
    result_location = arr[pos+3]
    arr[result_location] = op_result
    logging.debug(f"{result_location=} {op_result=}")
  else:
    logging.error(f"Write location parameter in immediate mode")
    return 0

  return 1


def op_inp(arr, pos, pmodes):
  inp = int(input("INP: "))
  if pmodes[0] == 0:
    dest = arr[pos+1]
    arr[dest] = inp
  else:
    logging.error(f"Write location parameter in immediate mode")
    return 0
  return 1


def op_out(arr, pos, pmodes):
  if pmodes[0] == 0:
    out_loc = arr[pos+1]
    logging.info(f"OUT: {arr[out_loc]}")
  else:
    out = arr[pos+1]
    logging.info(f"OUT: {out}")
  return 1


def op_halt(arr,pos, pmodes):
  logging.info(f"HALT")
  return None


OPERATIONS = {
         # Opcode: (function, num_params)
                1: (op_sum, 3),
                2: (op_mul, 3),
                3: (op_inp, 1),
                4: (op_out, 1),
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


def intcode(code):
  logging.info(f"Input code: {code}")
  pc = 0
  while True:
    instruction = code[pc]
    logging.debug(f"Processing {instruction=}")
    (opcode, param_modes) = read_instruction(instruction)
    try:
      logging.debug(f"Processing {opcode=}")
      (operation, num_params) = OPERATIONS[opcode]
      result = operation(code, pc, param_modes)
    except KeyError:
      logging.error(f"Invalid operation: {opcode=}")
      return
    if result:
      pc += (num_params+1)
    else:
      break

  logging.info(f"Processed program: {','.join(map(str,code))}")
  return code[0]
    
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
    code = list(map(int,line.split(',')))
    #operate(code, 12, 2)
    #find_result(19690720, code)
    intcode(code)
