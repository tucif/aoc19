#!/usr/bin/env python3
import logging
import fileinput
from itertools import chain, cycle, repeat

PATTERN = [0, 1, 0, -1]
def main():
  logging.basicConfig(level=logging.DEBUG)
  input_list, length = parse_input()
  offset = int(f"{''.join(str(o) for o in input_list[:7])}")
  logging.debug(f"{input_list=}")
  phase1_input = list(chain.from_iterable(repeat(input_list,1)))
  phase1_result = fft(phase1_input, length, PATTERN)
  input("Continue...")
  logging.debug(f"{input_list=}")
  phase2_input = input_list * 10_000
  phase2_result = fft2(phase2_input, offset)

def parse_input():
  for line in fileinput.input():
    l = [int(digit) for digit in line.rstrip()]
    return (l, len(l))

def fft(values, num_values, pattern=None, num_phases=100):
  phase = []
  logging.debug(f"{num_values=}")
  for phase_num in range(1,num_phases+1):
    patterns = (cycle(chain.from_iterable((repeat(p,times) for p in pattern))) for times in range(1,num_values+1))
    for i, curr_pattern in enumerate(patterns):
      # discard first
      next(curr_pattern)
      step_result = abs(sum((v * next(curr_pattern) for v in values))) % 10
      phase.append(step_result)
      # reset
      for r in range(len(pattern) - (len(phase) + 1 % len(pattern))):
        next(curr_pattern)
    values = phase
    phase=[]
  result = ''.join(str(x) for x in values[:8])
  logging.debug(f"{phase_num=} {result}")
  return result

def fft2(values, offset):
  for i in range(100):
    accum = 0 
    for v_i in range(len(values)-1, -1, -1):
      accum += values[v_i]
      values[v_i] = accum % 10
      if v_i < offset:
        break
  result = values[offset:offset+8]
  logging.info(f"{''.join(str(d) for d in result)=}")
  return result

if __name__ == '__main__':
  main()
