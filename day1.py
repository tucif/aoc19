#!/usr/bin/env python3
from math import floor
import fileinput
import logging

class Module(object):
  def __init__(self, mass):
    self.mass = int(mass)

  def get_fuel_required(self):
    fuel_required = floor(self.mass/3) - 2
    return fuel_required

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

