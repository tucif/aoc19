#!/usr/bin/env python3
import logging
import fileinput
from itertools import product

def op_sum(arr, pos):
  op_bin(arr, pos, lambda a,b: a+b)
  return 1

def op_mul(arr,pos):
  op_bin(arr, pos, lambda a,b: a*b)
  return 1

def op_bin(arr, pos, operation):
  result_location = arr[pos+3]
  first_operand_location = arr[pos+1]
  second_operand_location = arr[pos+2]

  first_operand = arr[first_operand_location]
  second_operand = arr[second_operand_location]

  op_result = operation(first_operand, second_operand)
  arr[result_location] = op_result
  return 1

def op_halt(arr,pos):
  return None

def intcode(opcodes):
  logging.info(f"Input opcodes: {opcodes}")
  operations = {  1: op_sum,
                  2: op_mul,
                 99: op_halt}
  pc = 0
  while True:
    opcode = opcodes[pc]
    try:
      result = operations[opcode](opcodes, pc)
    except KeyError:
      logging.error(f"Invalid operation: {opcode}")
      return
    if result:
      pc += 4
    else:
      break

  logging.info(f"Processed program: {','.join(map(str,opcodes))}")
  return opcodes[0]
    
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
    find_result(19690720, code)
