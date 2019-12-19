#!/usr/bin/env python3
import fileinput
import logging
from itertools import combinations
from math import gcd

class Moon(object):
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z
    self.velx = 0
    self.vely = 0
    self.velz = 0

  def update_relative_vel(self, other):
    if other.x > self.x:
      self.velx += 1
    elif other.x < self.x:
      self.velx -= 1
    if other.y > self.y:
      self.vely += 1
    elif other.y < self.y:
      self.vely -= 1
    if other.z > self.z:
      self.velz += 1
    elif other.z < self.z:
      self.velz -= 1

  def update_pos(self):
    self.x += self.velx
    self.y += self.vely
    self.z += self.velz

  def get_potential_energy(self):
    return abs(self.x) + abs(self.y) + abs(self.z)

  def get_kinetic_energy(self):
    return abs(self.velx) + abs(self.vely) + abs(self.velz)

  def get_total_energy(self):
    pot = self.get_potential_energy() 
    kin = self.get_kinetic_energy()
    total = pot * kin
    logging.debug(f"{pot=}; {kin=}; {total=}")
    return total

  def __repr__(self):
    pos = f"<x={self.x}, y={self.y}, z={self.z}>"
    vel = f"<x={self.velx}, y={self.vely}, z={self.velz}>"
    return f"{pos=} {vel=}"

  def __key(self):
    return (self.x, self.y, self.z, self.velx, self.vely, self.velz)

  # make sure it's hashable for phase2
  def __hash__(self):
    return hash(self.__key())

  def __eq__(self, other):
    if isinstance(other, Moon): return self.__key() == other.__key() 


def parse_input(inp = None):
  moons = []
  if inp is None:
    inp = fileinput.input()
  for line in inp:
    line = line.rstrip()
    logging.debug(f"{line=}")
    if not line:
      continue
    # also strip away initial '<' and trailing '>'
    moons.append(eval(f"Moon({line[1:-1]})"))
  return moons

def log_moons(moons):
  for moon in moons:
    logging.info(moon)

def apply_steps(moons, steps, logevery=1):
  for step in range(1,steps+1):
    for m1, m2 in combinations(moons, 2):
      # update moon1 values
      m1.update_relative_vel(m2)
      # update moon2 values
      m2.update_relative_vel(m1)
    # Update position at step end
    for moon in moons:
      moon.update_pos()
    if logevery and step % logevery == 0:
      logging.debug(f"After {step=}")
      log_moons(moons)

def get_total_system_energy(moons):
  total = 0
  for moon in moons:
    total += moon.get_total_energy()
  logging.info(f"Sum of total energy: {total}")
  return total

def get_axis_state(moons, axis):
  axis_values = []
  for moon in moons:
    if axis == 'x':
      axis_values.append(moon.x)
    elif axis == 'y':
      axis_values.append(moon.y)
    elif axis == 'z':
      axis_values.append(moon.z)
  return tuple(axis_values)
    

def get_all_axis_state(moons):
  axis_states = {}
  axis_states['x'] = get_axis_state(moons,'x')
  axis_states['y'] = get_axis_state(moons,'y')
  axis_states['z'] = get_axis_state(moons,'z')
  return axis_states

def get_lcm(x,y,z):
  # lcm(a,b) is a*b//gcd(a,b)
  # lcm is also commutative 
  lcm_xy = (x * y) // gcd (x,y)
  lcm_xyz = lcm_xy * z // gcd(lcm_xy, z)
  return lcm_xyz

def get_steps_until_repeated(moons):
  steps = 0
  initial_state = get_all_axis_state(moons)
  logging.debug(f"{initial_state=}")
  axis_periods = {}
  while True:
    apply_steps(moons, 1, 0)
    step_states = get_all_axis_state(moons)
    steps += 1
    if 'x' not in axis_periods and step_states['x'] == initial_state['x']:
      axis_periods['x'] = steps+1
    if 'y' not in axis_periods and step_states['y'] == initial_state['y']:
      axis_periods['y'] = steps+1
    if 'z' not in axis_periods and step_states['z'] == initial_state['z']:
      axis_periods['z'] = steps+1
    if ('x' in axis_periods and 
       'y' in axis_periods and
       'z' in axis_periods):
       break
  logging.debug(f"{steps=}")
  logging.debug(f"{axis_periods=}")

  lcm = get_lcm(axis_periods['x'], axis_periods['y'], axis_periods['z'])
  logging.debug(f"{lcm=}")

  return lcm
    

def main():
  logging.basicConfig(level=logging.DEBUG)
  moons = parse_input()
  logging.info(f"After step=0")
  log_moons(moons)
  #steps = 1000
  #apply_steps(moons, steps, logevery=1000)
  #return get_total_system_energy(moons)
  get_steps_until_repeated(moons)


if __name__ == '__main__':
  main()
