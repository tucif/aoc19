#!/usr/bin/env python3
import logging
import fileinput
from itertools import product
import sys
import re
from io import StringIO
from itertools import permutations
from itertools import cycle

from day2 import standalone
from day2 import Program

def main():
  logging.basicConfig(level=logging.INFO)
  for line in fileinput.input():
    program = Program(line)
    # phase 1
    evaluate_amplifiers(program)
    # phase 2
    #evaluate_amplifiers(program, 5, 9)
  

def evaluate_amplifiers(program, min_phase=0, max_phase=4):
  max_signal = 0
  max_phase_sequence = None
  phase_sequences = permutations(range(min_phase, max_phase+1)) 
  for sequence in phase_sequences:
    orig_sequence = sequence
    logging.info(f"Processing {sequence=}")

    signal = 0

    amplifiers = []
    for i in range(len(sequence)+1):
      code_copy = program.code.copy()
      program_copy = Program(code_copy)
      amplifiers.append( program_copy )

    if min_phase > 4:
      # feedback loop mode
      sequence = cycle(enumerate(sequence))
    else:
      sequence = enumerate(sequence)

    for i, (amplifier, phase) in enumerate(sequence):
      logging.info("*"*12 + f" Amplifier {chr(amplifier+65)}\n")
      
      if i < 5:
        # init with phase
        logging.info(f"{phase=}")
        logging.info(f"Input: {phase=}, {signal=}")
        initial_input = f"{phase}\n{signal}"
      else:
        logging.info(f"Input {signal=}")
        initial_input = f"{signal}"

      out = StringIO()
      # resume the amplifier at its last pc
      standalone(amplifiers[amplifier], initial_input, out)

      output = out.read().rstrip()
      logging.info(f"{output=}")
      out_match = re.search('(\d+)', output)
      if out_match:
        (signal,) = out_match.groups()
        logging.info(f"{signal=}")
      else:
        break

    if int(signal) > max_signal:
      max_signal = int(signal)
      max_phase_sequence = list(orig_sequence)

  logging.info(f"{max_phase_sequence=}") 
  logging.info(f"{max_signal=}") 
  return max_signal


if __name__ == '__main__':
  main()
