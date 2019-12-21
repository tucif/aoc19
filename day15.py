#!/usr/bin/env python3
import fileinput
import logging
from io import StringIO
from queue import Queue
from queue import LifoQueue
from enum import Enum

from day2 import Program, standalone

logger = logging.getLogger('Droid')
logger.setLevel(logging.INFO)

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
    system_location = None
    frontier = Queue()
    came_from = {}
    #self.location.type = Location.Type.PATH
    came_from[self.location.tuple] = None
    frontier.put(self.location)

    while not frontier.empty():
      logger.debug("")
      logger.debug(f"{frontier.queue=}")
      logger.debug("")
      logger.debug(f"{came_from.keys()=}")
      if system_location:
        break

      current = frontier.get()

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

          if status == self.Status.FOUND:
            neighbor.type = Location.Type.SYSTEM
            system_location = neighbor
            break
          elif status == self.Status.WALL:
            neighbor.type = Location.Type.WALL
          elif status == self.Status.MOVED:
            neighbor.type = Location.Type.PATH
            # only put paths into frontier for further exploration
            logger.debug(f"Adding {neighbor=} to frontier")
            frontier.put(neighbor)
            # move back to current
            logger.debug("Moving Back >>>")
            self.move(direction.opposite())
            logger.debug("Moved Back <<<")

      # move back
      self.move_to_origin(current)

    logger.info(f"{system_location=}")
    sl = system_location
    path_length = 0
    while sl.pred:
      path_length+=1
      sl = sl.pred
    logger.info(f"{path_length=}")
    return system_location

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
        logger.error(f"Found {status.name} while moving back from {curr} to origin")
      curr = curr.pred
    # TODO: sometimes does not move to real origin
    # probably because we modified some of the path's preds
    logger.debug(f"Moved to origin {self.location.tuple}<<<")


def main():
  logging.basicConfig(level=logging.ERROR)
  for line in fileinput.input():
    droid = RepairDroid(line)
    droid.find_oxygen_system()


if __name__ == '__main__':
  main()
