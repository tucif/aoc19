#!/usr/bin/env python3
import fileinput
import logging
from collections import namedtuple
from collections import defaultdict
from collections import Counter
from math import degrees, asin, sqrt, hypot, pi
from decimal import Decimal
from operator import itemgetter

def main():
  logging.basicConfig(level=logging.INFO)
  asteroids = process_input()
  (data, station) = find_best_station(asteroids)
  _200th = find_nth_vaporized(data, station, 200)
  logging.info(f"Answer={_200th.x * 100 + _200th.y}")


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
  data = defaultdict(lambda: defaultdict(list))
  #O(n**2) :(
  for station_candidate in asteroids:
    for asteroid in asteroids:
      if asteroid != station_candidate:
        (angle, distance) = get_angle_between(station_candidate, asteroid)
        data[station_candidate][angle].append((asteroid, distance))
  
  max_neighbors = 0
  station = None
  for candidate, angles in data.items():
    neighbors = len(angles)
    logging.debug(f"{candidate=} {neighbors=}")
    if neighbors > max_neighbors:
      max_neighbors = neighbors
      station = candidate

  logging.info(f"{station=} {max_neighbors=}")
  return (data, station)
      
def find_nth_vaporized(data, station, nth):
  nth_asteroid = None
  logging.debug(f"{len(data)}")
  station_neighbors = data[station]
  # sort asteroids by distance ascending
  for angle in station_neighbors:
    asteroids = station_neighbors[angle]
    if len(asteroids) < 2:
      continue
    station_neighbors[angle] = sorted( asteroids, key=itemgetter(1))
    logging.debug(f"Resorted: {station_neighbors[angle]=}")
  logging.debug(f"{len(station_neighbors)=}")
  angles = sorted(station_neighbors.keys())
  logging.debug(f"Sorted {angles=} {len(angles)=}")
  vaporizer_angle = 270
  for angle_idx , angle in enumerate(angles):
    if angle >= vaporizer_angle:
      break
  logging.debug(f"{angle_idx=}")

  vaporized = 0
  current_angle_idx = angle_idx
  while vaporized < len(data)-1:
    angle = angles[current_angle_idx]
    asteroids_at_angle = station_neighbors[angle]
    #logging.debug(f"{current_angle_idx=}{vaporized=}")
    current_angle_idx = (current_angle_idx + 1 ) % (len(angles))
    if not asteroids_at_angle:
      continue
    asteroid_vaporized = asteroids_at_angle.pop(0)
    vaporized += 1
    if vaporized == nth:
      nth_asteroid = asteroid_vaporized
    logging.debug(f"Vaporized #{vaporized} {asteroid_vaporized} at {angle=}. Remaining {asteroids_at_angle}")

  logging.info(f"#{nth} vaporized: {nth_asteroid}")
  return nth_asteroid[0]

    
    
def get_angle_between(a,b):
    x = b.x - a.x
    y = b.y - a.y
    hyp = hypot(x, y)
    # up or down
    if b.x == a.x:
      angle = 270 if b.y < a.y else 90
      return (Decimal(angle), hyp)
    # left or right
    if b.y == a.y:
      angle = 180 if b.x < a.x else 360
      return (Decimal(angle), hyp)
    slope = abs(b.y - a.y) / hyp
    if b.y > a.y:
      if b.x < a.x:
        angle = degrees(pi - asin(slope))
      else:
        angle = degrees(asin(slope))
    else:
      if b.x < a.x:
        angle = degrees(asin(slope) - pi)
        if angle < 0:
          angle = 360 + angle
      else:
        angle = degrees(2*pi - asin(slope))
    rounded_angle = round(Decimal(angle), 4)           
    logging.debug(f"{a} {rounded_angle} {b}")           
    return (rounded_angle, hyp)
  
if __name__ == '__main__':
  main()
