#!/usr/bin/env python3
import fileinput
import logging
from collections import namedtuple
from collections import defaultdict
from math import degrees, asin, sqrt, hypot
from decimal import Decimal

def main():
  logging.basicConfig(level=logging.INFO)
  asteroids = process_input()
  num_asteroids_detected = find_best_station(asteroids)


def process_input():
  asteroids = []
  P = namedtuple("Point",['x', 'y'])
  for col, line in enumerate(fileinput.input()):
    for row, char in enumerate(line):
      if char == '#':
        asteroids.append(P(row, col))
  logging.debug(f"{asteroids=}")
  return asteroids


def find_best_station(asteroids):
  data = defaultdict(set)
  #O(n**2) :(
  for station_candidate in asteroids:
    for asteroid in asteroids:
      if asteroid != station_candidate:
        angle = _get_angle_between(station_candidate, asteroid)
        data[station_candidate].add(angle) 
  
  max_neighbors = 0
  station = None
  for candidate, angles in data.items():
    neighbors = len(angles)
    logging.debug(f"{candidate=} {neighbors=}")
    if neighbors > max_neighbors:
      max_neighbors = neighbors
      station = candidate

  logging.info(f"{station=} {max_neighbors=}")
  return max_neighbors
      
  

def _get_angle_between(a,b):
    if b.x <= a.x and b.y <= a.y:                       
        base = 0                                        
        opposite = a.y - b.y                            
    elif b.x >= a.x and b.y >= a.y:                     
        base = 180                                      
        opposite = a.y - b.y                            
    elif b.x >= a.x and b.y <= a.y:                     
        base = 90                                       
        opposite = b.y - a.y                            
    elif b.x <= a.x and b.y >= a.y:                     
        base = 270                                      
        opposite = b.y - a.y                            
                                                        
    hyp = hypot(a.x - b.x, a.y - b.y)                   
    angle = degrees(asin(abs(opposite) / hyp))          
    angle += base                                       
    rounded_angle =  round(Decimal(angle), 4)           
    logging.debug(f"{a} {rounded_angle} {b}")           
    return rounded_angle
  
if __name__ == '__main__':
  main()
