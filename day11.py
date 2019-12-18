#!/usr/bin/env python3
import logging
import fileinput
import sys
import re
from io import StringIO
from collections import defaultdict
from collections import namedtuple
from pprint import pprint

from day2 import standalone
from day2 import Program

Loc = namedtuple('Location', ['x','y'])
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = ['UP','RIGHT','DOWN','LEFT']
COLORS = ['Black','White']

def main():
  logging.basicConfig(level=logging.INFO)
  for line in fileinput.input():
    program = Program(line)
    o = sys.stdout
    (panels_painted, xsize, ysize) = hull_painting(program, 1)
    sys.stdout = o
    logging.info(f"Phase 1: {len(panels_painted)} {xsize=} {ysize=}")
    render = render_panels(panels_painted, xsize, ysize)


def render_panels(panels, x, y):
  render = [0]*(y*2+1)
  for r in range(len(render)):
    render[r] = [0]*(x*2+1)

  for loc, color in panels.items():
    render[y+loc.y][x+loc.x] = color

  out = StringIO()
  for i in range(y*2,-1,-1):
    for j in range(x*2):
      color = render[i][j]
      out.write(f'{color}'.replace('0',' ').replace('1','#'))
    out.write('\n')

  out.seek(0)
  if sys.stdout.isatty():
    print(out.read())
    out.seek(0)

  return out.read()


def hull_painting(program, starting_color = 0):

  program.rewind_output = False

  panels_painted = {}
  current_panel = Loc(0,0)

  panels_painted[current_panel] = starting_color
  current_direction = UP

  # store sizes for rendering
  largest_x = 0
  largest_y = 0
  smallest_x = 0
  smallest_y = 0
  while True:
    # all panels black(0) by default
    camera = panels_painted.get(current_panel, 0)
    out = StringIO()
    inp = f"{camera}"

    # Run intcode, it'll suspend on input
    standalone(program, inp, out)

    output = out.read().rstrip().split("\n")
    if output[0]:
      (color,) = re.search('(\d+)', output[0]).groups()
      color = int(color)
      (turn,) = re.search('(\d+)', output[1]).groups()
      turn = int(turn)
      
      panels_painted[current_panel] = color
      logging.debug(f"Painted {current_panel} {COLORS[color]}")
      (current_panel, current_direction) = get_movement(current_panel, current_direction, turn)
      curr_x = current_panel.x
      curr_y = current_panel.y
      if curr_x > largest_x:
        largest_x = curr_x
      if curr_y > largest_y:
        largest_y = curr_y
      if curr_x < smallest_x:
        smallest_x = curr_x
      if curr_y < smallest_y:
        smallest_y = curr_y
      logging.debug(f"Turned {DIRECTIONS[current_direction]}")
    else:
      # halted
      break

  map_x = largest_x + abs(smallest_x)
  map_y = largest_y + abs(smallest_y)
  return (panels_painted, map_x, map_y)


def get_movement(current_location, current_direction, turn):
  movement = 1
  direction = None
  next_location = None
  next_x = current_location.x
  next_y = current_location.y
  if turn == 0:
    # left 90 degrees
    direction = (current_direction - 1) % 4
  else:
    # right 90 degrees
    direction = (current_direction + 1) % 4

  # Now that we've turned, move
  if direction == UP:
    next_y += movement
  elif direction == DOWN:
    next_y -= movement
  elif direction == RIGHT:
    next_x += movement
  elif direction == LEFT:
    next_x -= movement

  return (Loc(next_x, next_y), direction)

if __name__ == '__main__':
  main()
