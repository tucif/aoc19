#!/usr/bin/env python3
import logging
import fileinput
import sys
from io import StringIO

from day2 import Program, standalone

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_HPADDLE = 3
TILE_BALL = 4
TILE_NAMES = [' ','%','#','=','o']

def main():
  logging.basicConfig(level=logging.ERROR)
  for line in fileinput.input():
    program = Program(line, rw=0)
    #screen = init_game(program)
    #block_tiles = count_tiles(screen, TILE_BLOCK)
    #logging.info(f"{block_tiles=}")
    screen = {}
    run_game(program, screen)

def count_tiles(tiles, tileid):
  counter = 0
  for tile, tid in tiles.items():
    if tid == tileid:
      counter += 1
  return counter

def render_game(screen):
  out = StringIO()
  score = screen.get((-1,0), '-1')
  for y in range(21):
    for x in range(36):
      tileid = screen[(x,y)]
      out.write(f"{TILE_NAMES[tileid]}")
    out.write('\n')
  out.write(f"SCORE: {score}\n")
  

  if sys.stdout.isatty():
    out.seek(0)
    print(out.read())
    
def run_game(program, screen):
  # play for free
  program.code[0] = 2
  inp = "0"
  while True:
    out = StringIO()
    old_stdout = sys.stdout
    standalone(program, inp, out)
    (pad, ball) = update_screen(screen, out.read().split('\n'))
    sys.stdout = old_stdout
    render_game(screen)
    if ball is None:
      break
    # Make pad follow the ball, to play automatically
    if ball > pad:
      inp = "1"
    elif ball < pad:
      inp = "-1"
    else:
      inp = "0"
    #inp = input("Move joystick: ")
  
  

def update_screen(screen, tileinfo):
  ball_loc = None
  pad_loc = None
  game = []
  for output in tileinfo:
    output = output.rstrip()
    if output:
      game.append(output)
  #logging.debug(",".join(game))
  xsize = 0
  ysize = 0
  while game:
    x = int(game.pop(0))
    y = int(game.pop(0))
    tileid = int(game.pop(0))
    screen[(x,y)] = tileid
    if tileid == TILE_BALL:
      ball_loc = x
    if tileid == TILE_HPADDLE:
      pad_loc = x
    if x == -1:
      logging.info(f"Score: {tileid}")
    else:
      logging.info(f"({x},{y}): {TILE_NAMES[tileid]}")
    # store sizes for rendering
    if x > xsize:
      xsize = x
    if y > ysize:
      ysize = y

  logging.info(f"{xsize=}{ysize=}")
  return (pad_loc, ball_loc)

def init_game(program):
  out = StringIO()
  standalone(program, '', out)
  screen = {}
  update_screen(screen, out.read().split('\n'))
  return screen
  

if __name__ == '__main__':
  main()
