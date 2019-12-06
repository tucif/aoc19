#!/usr/bin/env python3
from math import floor
import fileinput
import logging

class Module(object):
  def __init__(self, mass):
    self.mass = int(mass)

  def get_fuel_required(self, account_for_fuel=True):
    fuel_required = self.get_mass_fuel_required()
    if not account_for_fuel:
      return fuel_required

    # Stage 2: account for fuel as part of mass
    remaining_fuel = fuel_required
    while remaining_fuel := self._get_fuel_for(remaining_fuel):
      fuel_required += remaining_fuel
    return fuel_required

  def get_mass_fuel_required(self):
    return self._get_fuel_for(self.mass)

  def _get_fuel_for(self, mass):
    return max(0, mass//3 - 2)

  def __str__(self):
    return f"Module(mass = {self.mass})"


class Spacecraft(object):
  def __init__(self, modules):
    self.modules = modules

  def add_module(self, module):
    self.modules.append(module)

  def get_fuel_required(self):
    return sum([module.get_fuel_required() for module in self.modules])


def process_input():
  logging.info("Expecting a module's mass per line. Finish with EOF/C-D.")
  craft = Spacecraft([Module(line) for line in fileinput.input()])
  fuel_req = craft.get_fuel_required()
  logging.info(f'{fuel_req=}')

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  process_input()

