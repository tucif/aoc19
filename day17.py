#!/usr/bin/env python3
import fileinput
import logging
import sys
from io import StringIO

from day2 import Program

logger = logging.getLogger('ASCII')
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
def main():
  for line in fileinput.input():
    r = VaccumRobot(line)
    r.build_scaffold_view()
    r.find_intersections()
    r.render_view()
    path = []
    r.dfs(path)
    # HACK: adding the last movement, as it wasn't added because no turn was made
    path.append(6)
    logger.info(f"{','.join(str(p) for p in path)=}")
    r = VaccumRobot(line)
    r.run_pattern(path)

class VaccumRobot:
  def __init__(self, map_data):
    self.program = Program(map_data, rw=0, output=StringIO())
    self.scaffold_view = None
    self.xsize = 0
    self.ysize = 0
    self.xposition = None
    self.yposition = None
    self.direction = '^'
    self.intersections = {}

  def build_scaffold_view(self):
    status = self.program.exec_standalone('')
    #self.render()

    x, y = 0, 0
    view = {}
    for line in self.program.output:
      pixel = int(line.strip())
      if pixel == ord('\n'):
        if y > self.ysize:
          self.ysize = y
        y+=1
        x = 0
      elif pixel == ord('^'):
        self.xposition = x
        self.yposition = y
      view[(x,y)] = pixel
      if x > self.xsize:
        self.xsize = x
      x+=1
    self.view = view
        
      
  def render_view(self):
    for y in range(self.ysize):
      for x in range(self.xsize):
        p = chr(self.view[(x,y)])
        if x == self.xposition and y == self.yposition:
          p = self.direction
        sys.stdout.write(p)
    sys.stdout.write('\n')

  def render(self):
    self.program.output.seek(0)
    for line in self.program.output:
      sys.stdout.write(chr(int(line.strip())))
    self.program.output.seek(0)

  def find_intersections(self):
    alignment_params = []
    for (x, y), pixel in self.view.items():
      if pixel == ord('#'):
        neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if all(self.view.get((nx,ny)) == ord('#') for nx,ny in neighbors):
          logger.debug(f"Intersection {x-1},{y}")
          self.intersections[(x,y)] = None
          alignment_params.append(abs((x-1)*y))
          #self.view[(x,y)] = 73
    calibration_code = sum(alignment_params)
    logger.debug(f"{calibration_code}")
    return calibration_code

  def opposite(self, direc):
    return {'^': 'v', '>':'<', '<':'>', 'v':'^'}[direc]

  def get_neighbors(self, favored_direction):
    x = self.xposition
    y = self.yposition
    # R D L U
    directions = ['>', 'v', '<', '^']
    index_favored = directions.index(favored_direction) 
    directions = directions[index_favored:] + directions[0:index_favored]
    neighbors = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]
    neighbors = neighbors[index_favored:] + neighbors[0:index_favored]
    return zip(directions, neighbors)
    

  def get_turn(self, new_dir):
    turn = None
    if (self.direction == '^' and new_dir == '>' or
        self.direction == '>' and new_dir == 'v' or
        self.direction == 'v' and new_dir == '<' or
        self.direction == '<' and new_dir == '^'):
      turn = 'R'
    if (self.direction == '^' and new_dir == '<' or
        self.direction == '<' and new_dir == 'v' or
        self.direction == 'v' and new_dir == '>' or
        self.direction == '>' and new_dir == '^'): turn =  'L'
    logger.debug(f"Turn from {self.direction} to {new_dir}: {turn}")
    return turn

  def dfs(self, path=None, movement=0, visited=None):
    if visited is None:
      visited = {}

    if path is None:
      path = []

    visited[ (self.xposition, self.yposition) ] = self.direction
    logger.debug(f"{self.xposition}, {self.yposition}")
    self.render_view()
    #import pdb; pdb.set_trace()

    for d, n in self.get_neighbors(self.direction):
      if n not in visited:
        if self.view.get(n) == ord('#'):
          self.xposition, self.yposition = n

          if d != self.direction:
            # turn
            turn = self.get_turn(d)
            if movement:
              path.append(movement)
            path.append(turn)
            movement = 0

          self.direction = d

          movement += 1

          self.dfs(path, movement, visited)
      else:
        if n in self.intersections:
          if visited[n] != self.direction:
            self.xposition, self.yposition = n
            self.direction = d

            movement += 1 

            self.dfs(path, movement, visited)
    # TODO:at the end of the path, we must add the movement even if there's no turn
    # thus need a way to detect we are at the end (probably all neighbors are '.' and prev is in visited)

  def run_pattern(self, path):
    input("PAUSE")
    #path = 'L,4,L,4,L,6,R,10,L,6,L,4,L,4,L,6,R,10,L,6,L,12,L,6,R,10,L,6,R,8,R,10,L,6,R,8,R,10,L,6,L,4,L,4,L,6,R,10,L,6,R,8,R,10,L,6,L,12,L,6,R,10,L,6,R,8,R,10,L,6,L,12,L,6,R,10,L,6'
    path = ','.join(str(p) for p in path)
    # These came from a suffix tree (online) ;) 
    # the longest paths (depth) are the longest common substrings
    A = 'L,4,L,4,L,6,R,10,L,6\n'
    B = 'R,8,R,10,L,6\n'
    C = 'L,12,L,6,R,10,L,6\n'
    pattern_path = "A,A,C,B,B,A,B,C,B,C\n"

    inputs = None
    newline = '\n'
    main_movement = f"{newline.join(list(str(ord(p)) for p in pattern_path))}"
    func_a = f"{newline.join(list(str(ord(p)) for p in A))}"
    func_b = f"{newline.join(list(str(ord(p)) for p in B))}"
    func_c = f"{newline.join(list(str(ord(p)) for p in C))}"
    video_feed = f"{ord('n')}{newline}10"
    inputs = f"{main_movement}\n{func_a}\n{func_b}\n{func_c}\n{video_feed}"
    logger.debug(f"{inputs=}")

    self.program.code[0] = 2 # get prompted for movement
    self.program.output.seek(0)
    self.program.output.truncate()
    self.program.exec_standalone(inputs)
    self.program.output.seek(0)
    outp = self.program.output.read()
    print(''.join([chr(int(line.rstrip())) for line in outp.split('\n') if line]))
    
    
if __name__ == '__main__':
  main()
