#!/usr/bin/env python3
import fileinput
import logging
import json
from collections import defaultdict



def main():
  logging.basicConfig(level=logging.DEBUG)
  wire_paths = parse_input()
  logging.debug(f"{wire_paths=}")
  intersection, distance = get_closest_intersection_distance(wire_paths)
  logging.info(f"Answer: {intersection=} \n{distance=}")
  
def parse_input():
  wires = []
  for line in fileinput.input():
    wires.append(line.split(","))
    if len(wires) == 2:
      break
  return wires

def get_closest_intersection_distance(wire_paths):
  intersections = get_wire_intersections(wire_paths)
  closest_distance = None
  closest_intersection = None
  center = (0,0)
  for intersection in intersections:

    intersection_distance = get_manhattan_distance(center, intersection)
      
    if not closest_distance or intersection_distance < closest_distance:
      closest_distance = intersection_distance
      closest_intersection = intersection
      continue

  return (closest_intersection, closest_distance)
       
def get_wire_intersections(wire_paths):
  intersections = set()
  # locations are a hash of horizonal levels visited
  # each with a hash of vertical levels visited at that horizontal level
  # each with how many wires were found there
  wire_locations = defaultdict(lambda: defaultdict(set))

  for wire_number, wire_movements in enumerate(wire_paths):
    # Paths can be UX, DX, LX, RX
    # with X indicating the number of steps in that direction
    # horizontal movement
    h = 0
    # vertical movement
    v = 0
    for movement in wire_movements:
      logging.debug(f"Processing {movement=}")
      direction = movement[0].upper()
      magnitude = int(movement[1:])
      if direction == 'R':
        # Process positive horizontal movement
        for i in range(0, magnitude+1):
          wire_locations[h+i][v].add(wire_number)
          if len(wire_locations[h+i][v]) > 1:
            intersections.add((h+i,v)) 
        h += magnitude
      elif direction == 'L':
        # Process negative horizontal movement
        for i in range(0, magnitude+1):
          wire_locations[h-i][v].add(wire_number)
          if len(wire_locations[h-i][v]) > 1:
            intersections.add((h-i,v)) 
        h -= magnitude
      elif direction == 'U':
        # Process positive vertical movement
        for i in range(0, magnitude+1):
          wire_locations[h][v+i].add(wire_number)
          if len(wire_locations[h][v+i]) > 1:
            intersections.add((h,v+i)) 
        v += magnitude
      elif direction == 'D':
        # Process negative vertical movement
        for i in range(0, magnitude+1):
          wire_locations[h][v-i].add(wire_number)
          if len(wire_locations[h][v-i]) > 1:
            intersections.add((h,v-i)) 
        v -= magnitude
      #logging.debug(f"{wire_locations=}")

  # Intersection at center is invalid
  if (0,0) in intersections:
    intersections.remove((0,0))
    
  #logging.debug(f"{wire_locations=}")
  logging.debug(f"{intersections=}")

  return intersections
      

def get_manhattan_distance(p, q):
  return abs(p[0] - q[0]) + abs(p[1] - q[1])


 
if __name__ == "__main__":
  main()
