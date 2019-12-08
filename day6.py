#!/usr/bin/env python3
import fileinput
import logging

def main():
  logging.basicConfig(level=logging.DEBUG)
  orbits = process_input()
  space_objects = {}
  checksum = get_orbit_checksum(orbits, space_objects)
  logging.info(f"{checksum=}")
  transfers = find_orbital_transfers(space_objects, 
                         space_objects['YOU'], space_objects['SAN'])
  logging.info(f"{transfers=}")


def process_input():
  orbits = []
  for line in fileinput.input():
    (orbiting_name, orbiter_name) = line.rstrip().split(")")
    orbits.append((orbiting_name,orbiter_name))
  return orbits

class SpaceObject(object):
  def __init__(self, name, orbiting = None):
    self.name = name
    self.orbiting = orbiting

  def get_direct_indirect_orbits(self):
    orbits = 0
    if self.orbiting:
      # direct 
      orbits+=1
      # indirect
      orbits += self.orbiting.get_direct_indirect_orbits()

    return orbits
  
  
  def get_weighted_path_to(self, obj_name):
    weight = 0
    path = {}
    ancestor = self.orbiting
    while ancestor.name != obj_name:
      path[ancestor.name] = (ancestor.name, weight)
      weight += 1
      ancestor = ancestor.orbiting

    return path


  def __repr__(self):
    return f"{self.name}"
      

def get_orbit_checksum(orbits, space_objects):
  checksum = 0
  for orbiting_name, orbiter_name in orbits:
    orbiting = space_objects.get(orbiting_name, 
                                SpaceObject(orbiting_name))
    orbiter = space_objects.get(orbiter_name, 
                                SpaceObject(orbiter_name))

    orbiter.orbiting = orbiting
    space_objects[orbiting_name] = orbiting
    space_objects[orbiter_name] = orbiter


  for name, obj in space_objects.items():
    local_checksum = obj.get_direct_indirect_orbits()
    logging.debug(f"{name=}; ({local_checksum})")
    checksum += local_checksum

  #logging.debug(f"{space_objects=}")
  return checksum
  
def find_orbital_transfers(space_objects, a, b):
  a_path = a.get_weighted_path_to('COM')
  logging.debug(f"{a_path=}")
  b_path = b.get_weighted_path_to('COM')
  logging.debug(f"{b_path=}")
 
  intersections = []
  for obj_name, orbits in a_path.items():
    if obj_name in b_path:
      #intersection
      combined_orbits = a_path[obj_name][1] + b_path[obj_name][1]
      intersections.append((obj_name, combined_orbits))

  logging.debug(f"{intersections=}")
  # closest intersection is the one with least orbits
  (lowest_common_ancestor, transfers ) = min(intersections, key = lambda x: x[1])

  logging.debug(f"{lowest_common_ancestor=} {transfers=}")
  return transfers
    
  
if __name__ == '__main__':
  main()
