#!/usr/bin/env python3
import logging
import fileinput
from itertools import product
import sys
import re
from io import StringIO
from itertools import permutations
from itertools import cycle

from day2 import intcode

def main():
  logging.basicConfig(level=logging.INFO)
  for line in fileinput.input():
    code = list(map(int,line.split(',')))
    # phase 1
    #evaluate_amplifiers(code)
    # phase 2
    evaluate_amplifiers(code, 5, 9)
  

def evaluate_amplifiers(code, min_phase=0, max_phase=4):
  orig_stdin = sys.stdin
  orig_stdout = sys.stdout
  max_signal = 0
  max_phase_sequence = None
  phase_sequences = permutations(range(min_phase, max_phase+1)) 
  for sequence in phase_sequences:
    logging.info(f"Processing {sequence=}")

    feedback_mode = False
    signal = 0
    if min_phase > 4:
      # feedback loop mode
      feedback_mode = True
      amplifiers = []
      for i in range(len(sequence)+1):
        amplifiers.append( code[:] )

      sequence = cycle(enumerate(sequence))
      #sequence = sequence * 3


    # all amplifiers start at pc = 0
    pcs = [0] * len(amplifiers)
    for i, (amplifier, phase) in enumerate(sequence):
      logging.info("*"*12 + f" Amplifier {chr(amplifier+65)}\n")
      
      if i < 5:
        # init with phase
        logging.info(f"{phase=}")
        logging.info(f"Input: {phase=}, {signal=}")
        sys.stdin = StringIO(f"{phase}\n{signal}\n")
      else:
        logging.info(f"Input {signal=}")
        sys.stdin = StringIO(f"{signal}\n")

      sys.stdout = StringIO()
      # resume the amplifier at its last pc
      last_pc = intcode(amplifiers[amplifier], pcs[amplifier])
      pcs[amplifier] = last_pc

      output = sys.stdout.read().rstrip()
      logging.info(f"{output=}")
      out_match = re.search('(\d+)', output)
      if out_match:
        (signal,) = out_match.groups()
        logging.info(f"{signal=}")
      else:
        break
      #halt_match = re.search('(HALT)',  output)

      # reset stdout for next read
      sys.stdout.seek(0)
      sys.stdout.truncate()

      #if halt_match and feedback_mode:
      #  logging.debug("HALT from feedback mode")
      #  break

    if int(signal) > max_signal:
      max_signal = int(signal)
      max_phase_sequence = sequence

  # set back stdout to print result
  sys.stdout = orig_stdout
  logging.info(f"{max_phase_sequence=}") 
  logging.info(f"{max_signal=}") 


if __name__ == '__main__':
  main()
