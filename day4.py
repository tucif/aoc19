#!/usr/bin/env python3
import fileinput 
import logging

def main():
  logging.basicConfig(level=logging.DEBUG)
  inp = input("low, high: ")
  (low, high) = inp.split('-')
  low = int(low)
  high = int(high)
  logging.debug(f"{low=},{high=}")

  passwords = find_passwords(low, high, True)
  logging.debug(f"{passwords=}")


def find_passwords(low,high, ignore_larger_groups=False):
  search_space = high-low
  logging.debug(f"{search_space=}")
  matches = 0
  for i in range(high - low + 1):
    candidate = str(low+i)
    lastdigit = -1
    longest_repeated = 0
    match = True
    doubles = {}
    for digit in candidate:
      digit = int(digit)

      if digit < lastdigit:
        match = False
      if digit == lastdigit:
        longest_repeated += 1
      else:
        longest_repeated = 1

      if longest_repeated == 2:
        doubles[digit] = True

      # Phase 2
      if ignore_larger_groups:
        if longest_repeated > 2:
          if digit in doubles:
            del doubles[digit] 

      lastdigit = digit

    if len(doubles.keys()) < 1:
      match = False
    if match:
      logging.debug(f"Match: {candidate=}")
      matches+=1

  return matches

if __name__ == '__main__':
  main()
