#!/usr/bin/env python3
import fileinput
import logging

def main():
  logging.basicConfig(level=logging.DEBUG)
  orbits = process_input()
  checksum = get_orbit_checksum(orbits)
  logging.info(f"{checksum=}")


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

  def __repr__(self):
    return f"{self.name}"
      

def get_orbit_checksum(orbits):
  space_objects = {}
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
    logging.debug(f"{orbiter=}; ({local_checksum})")
    checksum += local_checksum

  #logging.debug(f"{space_objects=}")
  return checksum
  
  
if __name__ == '__main__':
  main()
