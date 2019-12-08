#!/usr/bin/env python3
import logging
import fileinput
from itertools import product
import sys
import re
from io import StringIO
from itertools import permutations

from day2 import intcode

def main():
  logging.basicConfig(level=logging.INFO)
  for line in fileinput.input():
    code = list(map(int,line.split(',')))
    evaluate_amplifiers(code)
  

def evaluate_amplifiers(code):
  orig_stdin = sys.stdin
  orig_stdout = sys.stdout
  max_signal = 0
  max_phase_sequence = None
  for sequence in permutations(range(5)):
    logging.info(f"Processing {sequence=}")
    # override stdout
    my_out = StringIO()
    sys.stdout = my_out

    signal = 0
    for phase in sequence:
      amplifier_code = code[:]
      sys.stdin = StringIO(f"{phase}\n{signal}")
      intcode(amplifier_code)
      my_out.seek(0)
      (signal,) = re.search('OUT: (\d+)', my_out.read()).groups()
      my_out.seek(0)
      my_out.truncate()

    if int(signal) > max_signal:
      max_signal = int(signal)
      max_phase_sequence = sequence

  # set back stdout to print result
  sys.stdout = orig_stdout
  logging.info(f"{max_phase_sequence=}") 
  logging.info(f"{max_signal=}") 


if __name__ == '__main__':
  main()
