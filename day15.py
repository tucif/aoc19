#!/usr/bin/env python3
import fileinput
import logging
import sys
from io import StringIO
from queue import Queue
from queue import PriorityQueue
from queue import LifoQueue
from collections import defaultdict
from enum import Enum

from day2 import Program, standalone

logger = logging.getLogger('Droid')
logger.setLevel(logging.ERROR)

class Direction(Enum):
  NORTH = 1
  SOUTH = 2
  WEST  = 3
  EAST  = 4

  def opposite(self):
    if self == self.NORTH:
      return self.SOUTH
    elif self == self.SOUTH:
      return self.NORTH
    elif self == self.EAST:
      return self.WEST
    elif self == self.WEST:
      return self.EAST
  

class Location:
  class Type(Enum):
    WALL = 0
    PATH = 1
    SYSTEM = 2

    def symbol(self):
      symb = {self.WALL.value: '#', 
              self.PATH.value: ' ', 
              self.SYSTEM.value:'O'}
      return symb[self.value]

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self._type = None
    self._pred = None
    self._pred_direction = None

  @property
  def type(self):
    return self._type

  @type.setter
  def type(self, t):
    self._type = t

  @property
  def pred(self):
    return self._pred

  @pred.setter
  def pred(self, p):
    self._pred = p

  @property
  def pred_direction(self):
    ''' direction which if followed from self leads to self.pred'''
    return self._pred_direction

  @pred_direction.setter
  def pred_direction(self, p):
    self._pred_direction = p

  @property
  def tuple(self):
    return self.__key()

  def update(self, direction):
    if direction == Direction.NORTH:
      self.y += 1
    elif direction == Direction.SOUTH:
      self.y -= 1
    elif direction == Direction.EAST:
      self.x += 1
    elif direction == Direction.WEST:
      self.x -= 1

  def get_neighbors(self):
    neighbors = []
    for direction in Direction:
      loc = Location(self.x, self.y)
      loc.update(direction)
      neighbors.append((loc, direction))
    return neighbors
           

  def copy(self):
    l = Location(self.x, self.y)
    l.type = self.type
    l.pred = self.pred
    return l

  def __key(self):
    return (self.x, self.y)

  def __hash__(self):
    return hash(self.__key())

  def __eq__(self, other):
    return self.__key() == other.__key()

  def __lt__(self, other):
    #manhattan distance 
    origin_from_self = abs(self.x) + abs(self.y)
    origin_from_other = abs(other.x) + abs(other.y)
    return origin_from_self < origin_from_other

  def __repr__(self):
    return f"({self.x},{self.y})[{self.type}]"


class RepairDroid(object):
  class Status(Enum):
    WALL  = 0
    MOVED = 1
    FOUND = 2

  def __init__(self, code):
    self.program = Program(code)
    self.location = Location(0,0)
    
  def find_oxygen_system(self):
    old_out = sys.stdout
    system_location = None
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    #self.location.type = Location.Type.PATH
    came_from[self.location.tuple] = None
    self.explored = {}
    cost_so_far[self.location.tuple] = 0
    frontier.put((0,self.location))
    # cheat: known location of oxygen system to use A*
    oxy_loc = Location(-20, -14)

    while not frontier.empty():
      logger.debug("")
      logger.debug(f"{frontier.queue=}")
      logger.debug("")
      logger.info(f"{len(came_from.keys())=}")
      logger.debug(f"{cost_so_far=}")

      priority, current = frontier.get()

      # move to current
      self.move_to_location(current)

      # explore neighbors  
      neighbors = current.get_neighbors()
      for neighbor, direction in neighbors:

        if neighbor.tuple not in came_from:

          status = self.move(direction)

          # to get to pred from neighbor, follow opposite direction
          neighbor.pred = current
          neighbor.pred_direction = direction.opposite()
          came_from[neighbor.tuple] = current
          self.explored[neighbor] = True

          if status == self.Status.FOUND:
            neighbor.type = Location.Type.SYSTEM
            system_location = neighbor
            new_cost = cost_so_far[current.tuple] + 1
            cost_so_far[system_location.tuple] = new_cost
            self.move(direction.opposite())
            break
          elif status == self.Status.WALL:
            neighbor.type = Location.Type.WALL
          elif status == self.Status.MOVED:
            neighbor.type = Location.Type.PATH
            # move back to current
            logger.debug("Moving Back >>>")
            self.move(direction.opposite())
            logger.debug("Moved Back <<<")
            # only put paths into frontier for further exploration
            new_cost = cost_so_far[current.tuple] + 1
            logger.info(f"{new_cost=} {neighbor.tuple in cost_so_far}")
            if (neighbor.tuple not in cost_so_far or 
                new_cost < cost_so_far[neighbor.tuple]):
              cost_so_far[neighbor.tuple] = new_cost
              heuristic = (abs(oxy_loc.x - neighbor.x) +
                           abs(oxy_loc.y - neighbor.y))
              priority =  new_cost + heuristic
              logger.debug(f"Adding {neighbor=} to frontier")
              frontier.put((priority, neighbor))


      sys.stdout = old_out
      self.render()
      if system_location:
        break

      # move back
      self.move_to_origin(current)

    logger.info(f"{system_location=}")
    logger.info(f"{cost_so_far[system_location.tuple]}")
    return system_location

  def render(self):
    size = 48
    mid = size//2
    screen =[['.'] * size for i in range(size)]
     
    for loc in self.explored.keys():
      symbol = loc.type.symbol()
      if loc.tuple == self.location.tuple:
        symbol = '@'
      screen[mid+loc.y][mid+loc.x] = symbol

    output = StringIO()
    for y in range(size):
      for x in range(size):
        output.write(f"{screen[y][x]}")
      output.write('\n')
    output.seek(0)
    print(output.read())

  def move(self, d):
    direction = Direction(d)
    inp = f"{direction.value}"
    out = StringIO()
    logger.debug(f"Moving {direction.name}")
    standalone(self.program, inp, out)
    status = self.Status(int(out.read().rstrip()))
    logger.debug(f"({status.name})")

    if status in [self.Status.MOVED, self.Status.FOUND]:
      self.location.update(direction)
    return status

  def move_to_location(self, location):
    logger.debug(f"Moving to {location=} >>>")
    path = LifoQueue()
    curr = location

    while curr.pred:
      if curr == self.location:
        break
      # to move from origin, follow opposite directions
      path.put(curr.pred_direction.opposite())
      curr = curr.pred

    while not path.empty():
      next_direction = path.get()
      self.move(next_direction)

    logger.debug(f"Moved to {self.location.tuple} <<<")

  def move_to_origin(self, curr):
    logger.debug(f"Moving to origin from {curr} >>>")
    while curr.pred:
      # to move to origin, follow pred direction
      status = self.move(curr.pred_direction)
      if status != self.Status.MOVED:
        # early exit
        break
      curr = curr.pred
    logger.debug(f"Moved to origin {self.location.tuple}<<<")


def main():
  logging.basicConfig(level=logging.ERROR)
  for line in fileinput.input():
    droid = RepairDroid(line)
    droid.find_oxygen_system()


if __name__ == '__main__':
  main()
