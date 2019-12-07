#!/usr/bin/env python3
import fileinput 
import logging

def main():
  logging.basicConfig(level=logging.DEBUG)
  inp = input("low, high: ")
  (low, high) = inp.split(',')
  low = int(low)
  high = int(high)
  logging.debug(f"{low=},{high=}")

  passwords = find_passwords(low, high)
  logging.debug(f"{passwords=}")


def find_passwords(low,high):
  highest = 567899
  lowest = 112345
  #if high > highest:
  #  high = highest
  #if low < lowest:
  #  low = lowest

  search_space = high-low
  logging.debug(f"{search_space=}")
  matches = 0
  for i in range(high - low + 1):
    candidate = str(low+i)
    doubles = 0
    if candidate[0] == candidate[1]:
      doubles += 1
    if candidate[1] == candidate[2]:
      doubles += 1
    if candidate[2] == candidate[3]:
      doubles += 1
    if candidate[3] == candidate[4]:
      doubles += 1
    if candidate[4] == candidate[5]:
      doubles += 1
  
    if doubles < 1:
      continue


    if ((candidate[1] > candidate[0] or candidate[1] == candidate[0]) and
       (candidate[2] > candidate[1] or candidate[2] == candidate[1]) and
       (candidate[3] > candidate[2] or candidate[3] == candidate[2]) and
       (candidate[4] > candidate[3] or candidate[4] == candidate[3]) and
       (candidate[5] > candidate[4] or candidate[5] == candidate[4]) ):
      matches += 1
      logging.debug(f"Match: {candidate=}")

  return matches

if __name__ == '__main__':
  main()
