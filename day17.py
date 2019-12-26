#!/usr/bin/env python3
import fileinput
import logging
import sys
from io import StringIO

from day2 import Program

logger = logging.getLogger('ASCII')
logger.setLevel(logging.DEBUG)
def main():
  for line in fileinput.input():
    r = VaccumRobot(line)
    r.build_scaffold_view()
    r.find_intersections()
    r.render_view()

class VaccumRobot:
  def __init__(self, map_data):
    self.program = Program(map_data, rw=0, output=StringIO())
    self.scaffold_view = None
    self.xsize = 0
    self.ysize = 0

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
      view[(x,y)] = pixel
      if x > self.xsize:
        self.xsize = x
      x+=1
    self.view = view
        
      
  def render_view(self):
    logger.debug(f"{self.xsize}, {self.ysize}")
    for y in range(self.ysize):
      for x in range(self.xsize):
        p = chr(self.view[(x,y)])
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
          alignment_params.append(abs((x-1)*y))
          self.view[(x,y)] = 73
    calibration_code = sum(alignment_params)
    logger.debug(f"{calibration_code}")
    return calibration_code



     
    
  
if __name__ == '__main__':
  main()
