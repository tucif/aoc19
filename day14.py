#!/usr/bin/env python3
import fileinput
import logging
import re
from collections import defaultdict
from io import StringIO

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
    self.stock = defaultdict(int)

  def parse_reactions(self, reactions):
    chemicals = {}
    production_rules = reactions.rstrip().split('\n')
    for production_rule in production_rules:
      recipe, product = production_rule.split('=>')
      recipe = recipe.strip()
      batch_size, name = product.strip().split()
      chemicals[name] = Chemical(name, batch_size, recipe)
    return chemicals

  def get_ore_used(self):
    return abs(self.stock['ORE'])

  def has_chemical_in_stock(self, name, amount):
    if name == 'ORE':
      return True
    return self.stock[name] >= amount

  def consume_chemical(self, name, amount):
    # non ORE shouldn't be allowed below 0
    self.stock[name] -= amount

  def produce_chemical(self, name, amount):
    while not self.has_chemical_in_stock(name, amount):
      # produce a batch of {name} until there's enough in stock
      chemical = self.chemicals.get(name)
      for ingredient in chemical.recipe:
        self.produce_chemical(ingredient.name, ingredient.amount)
        self.consume_chemical(ingredient.name, ingredient.amount)
      self.stock[chemical.name] += chemical.batch_size
    
  def __repr__(self):
    return f"NanoFactory({self.chemicals})"


def main():
  logging.basicConfig(level=logging.DEBUG)
  s = StringIO()
  for line in fileinput.input():
    s.write(line)
  s.seek(0)
  factory = NanoFactory(s.read())
  factory.produce_chemical('A', 10)
  logging.debug(f"{factory=}")
  logging.debug(f"{factory.stock=}")
  logging.info(f"{factory.get_ore_used()}")
  

if __name__ == '__main__':
  main()
