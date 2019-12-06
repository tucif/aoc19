#!/usr/bin/env python3
import fileinput
import logging
import json
from collections import defaultdict
import re



def main():
  logging.basicConfig(level=logging.DEBUG)
  wire_paths = parse_input()
  logging.debug(f"{wire_paths=}")
  intersection, distance = get_closest_intersection_distance(wire_paths, 'steps')
  logging.info(f"Answer: {intersection=} \n{distance=}")
  
def parse_input():
  wires = []
  for line in fileinput.input():
    wires.append(line.split(","))
    if len(wires) == 2:
      break
  return wires

def get_closest_intersection_distance(wire_paths, method='manhattan'):
  intersections = get_wire_intersections(wire_paths)
  closest_distance = None
  closest_intersection = None
  center = '0H0V'
  for location,steps in intersections:

    if method == 'manhattan':
      intersection_distance = get_manhattan_distance(center, location)
    elif method == 'steps':
      intersection_distance = steps
      
    if not closest_distance or intersection_distance < closest_distance:
      closest_distance = intersection_distance
      closest_intersection = location
      continue

  return (closest_intersection, closest_distance)
       
def get_wire_intersections(wire_paths):
  intersections = []
  # locations are a hash of horizonal levels visited
  # each with a hash of vertical levels visited at that horizontal level
  # each with how many wires were found there
  wire_locations = defaultdict(set)

  for wire_number, wire_movements in enumerate(wire_paths):
    # Paths can be UX, DX, LX, RX
    # with X indicating the number of steps in that direction
    # horizontal movement
    h = 0
    # vertical movement
    v = 0
    steps = 0
    for movement in wire_movements:
      logging.debug(f"Processing {movement=}")
      direction = movement[0].upper()
      magnitude = int(movement[1:])
      if direction == 'R':
        # Process positive horizontal movement
        for i in range(0, magnitude+1):
          loc = f'{h+i}H{v}V'
          wire_locations[loc].add((wire_number, steps+i))
        h += magnitude
      elif direction == 'L':
        # Process negative horizontal movement
        for i in range(0, magnitude+1):
          loc = f'{h-i}H{v}V'
          wire_locations[loc].add((wire_number, steps+i))
        h -= magnitude
      elif direction == 'U':
        # Process positive vertical movement
        for i in range(0, magnitude+1):
          loc = f'{h}H{v+i}V'
          wire_locations[loc].add((wire_number, steps+i))
        v += magnitude
      elif direction == 'D':
        # Process negative vertical movement
        for i in range(0, magnitude+1):
          loc = f'{h}H{v-i}V'
          wire_locations[loc].add((wire_number, steps+i))
        v -= magnitude
      #logging.debug(f"{wire_locations=}")
      steps += magnitude


  # Intersection at center is invalid
  if '0H0V' in wire_locations:
    del wire_locations['0H0V']

  # Check locations for intersections
  for loc, wires in wire_locations.items():
    if len(wires) < 2:
      # can't possibly be an intersection 
      # as only 1 wire visited the location
      continue
  
    # intersection probably found
    # calculate sum of steps of all intersecting wires
    combined_steps = 0
    unique_wires = {}
    for wire, steps in wires:
      unique_wires[wire] = True
      combined_steps += steps

    if len(unique_wires) < 2:
      # not an intersection, just a wire crossing itself
      continue
    
    logging.debug(f'Intersection: {loc=} {wires=} {combined_steps=}')
    intersection = (loc, combined_steps)
    intersections.append(intersection)
    
  return intersections
      

def get_manhattan_distance(p, q):
  pattern = '(-?\d+)H(-?\d+)V'
  (p0, p1) = re.findall(pattern, p)[0]
  (q0, q1) = re.findall(pattern, q)[0]
  return abs(int(p0) - int(q0)) + abs(int(p1) - int(q1))


 
if __name__ == "__main__":
  main()
