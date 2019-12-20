#!/usr/bin/env python3
import fileinput
import logging
import re
from collections import defaultdict
from io import StringIO
from math import ceil

class Ingredient(object):
  def __init__(self, name, amount):
    self.name = name
    self.amount = int(amount)

  def __repr__(self):
    return f"{self.name}({self.amount})"

class Chemical(object):
  def __init__(self, name, batch_size, recipe):
    self.name = name
    self.batch_size = int(batch_size)
    self.recipe = self.parse_recipe(recipe)

  def parse_recipe(self, recipe):
    ingredients = []
    if not recipe:
      return ingredients
    components = recipe.split(',')
    for component in components:
      match = re.search('(\d+) (\w+)', component)
      amount, name = match.groups()
      ingredients.append(Ingredient(name, amount))
    return ingredients

  def __repr__(self):
    return f"{self.__class__.__name__}(batch_size={self.batch_size}, recipe={self.recipe}"
    
class NanoFactory(object):
  def __init__(self, reactions):
    self.chemicals = self.parse_reactions(reactions)
    self.reset_stock()

  def parse_reactions(self, reactions):
    chemicals = {'ORE': Chemical('ORE',1,'')}
    production_rules = reactions.rstrip().split('\n')
    for production_rule in production_rules:
      recipe, product = production_rule.split('=>')
      recipe = recipe.strip()
      batch_size, name = product.strip().split()
      chemicals[name] = Chemical(name, batch_size, recipe)
    return chemicals

  def get_ore_used(self):
    return abs(self.stock['ORE'])

  def reset_stock(self):
    self.stock = defaultdict(int)

  def has_chemical_in_stock(self, name, amount):
    if name == 'ORE':
      return True
    return self.stock[name] >= amount

  def consume_chemical(self, name, amount, indent=1):
    # non ORE shouldn't be allowed below 0
    self.stock[name] -= amount
    indentation = '\t' * indent
    logging.debug(f"{indentation}Consumed {amount} of {name}, remaining: {self.stock[name]}")

  def produce_chemical(self, name, amount, indent=1):
    indentation = '\t' * indent
    chemical = self.chemicals.get(name)
    stock = self.stock[chemical.name]
    original_amount = amount
    if name != 'ORE':
      # update amount required with stock
      amount -= stock
    batches = ceil(amount / chemical.batch_size)
    logging.debug(f"{indentation}producing {name}: needs {amount} (after taking {stock} from stock), make {batches=} of {chemical.batch_size} each")
    if not self.has_chemical_in_stock(name, original_amount):
      for ingredient in chemical.recipe:
        self.produce_chemical(ingredient.name, batches * ingredient.amount, indent+1)
        self.consume_chemical(ingredient.name, batches * ingredient.amount, indent+1)
      self.stock[chemical.name] += batches * chemical.batch_size
    else:
      logging.debug(f"{indentation}produced {name}: needs {amount=} has {self.stock[name]} in stock")
    
  def __repr__(self):
    return f"NanoFactory({self.chemicals})"

  def max_fuel_with_ore(self, total_ore, ore_per_fuel, fuel_low, fuel_high):
    logging.debug(f"Searching bewteen {fuel_low:,} and {fuel_high:,}")
    self.reset_stock()
    fuel_mid = fuel_low + (fuel_high - fuel_low) // 2
    self.produce_chemical('FUEL', fuel_mid)
    ore = self.get_ore_used()
    logging.debug(f"Can produce {fuel_mid:,} with {ore=:,}")
    if ore > total_ore:
      return self.max_fuel_with_ore(total_ore, ore_per_fuel, fuel_low, fuel_mid)
    elif ore < total_ore - ore_per_fuel:
      return self.max_fuel_with_ore(total_ore, ore_per_fuel, fuel_mid, fuel_high)
    else:
      return fuel_mid
     




def main():
  logging.basicConfig(level=logging.INFO)
  s = StringIO()
  for line in fileinput.input():
    s.write(line)
  s.seek(0)
  factory = NanoFactory(s.read())
  logging.debug(f"{factory=}")
  factory.produce_chemical('FUEL', 1)
  ore_per_fuel = factory.get_ore_used()
  logging.debug(f"{factory.stock=}")
  logging.info(f"{ore_per_fuel=}")
  factory.reset_stock()
  one_trillion = 1_000_000_000_000
  starting_fuel = one_trillion // ore_per_fuel
  max_fuel = factory.max_fuel_with_ore(one_trillion, ore_per_fuel, starting_fuel//2, starting_fuel*2)
  logging.info(f"{max_fuel=}")
  

if __name__ == '__main__':
  main()
