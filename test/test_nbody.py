import unittest
from test.lib import TestDay

from day12 import parse_input, apply_steps, get_total_system_energy
from day12 import get_steps_until_repeated

class TestDay12(TestDay):
  def _invoke(self, inp, steps, expected):
    moons = parse_input(inp.split('\n'))
    apply_steps(moons, steps)
    energy = get_total_system_energy(moons)
    self.assertEqual(energy, expected)

  def _invoke2(self, inp, expected):
    moons = parse_input(inp.split('\n'))
    steps = get_steps_until_repeated(moons)
    self.assertEqual(steps, expected)

    
  # samples
  def test_input1(self):
    inp = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''
    self._invoke(inp, steps=10, expected=179)
    self._invoke2(inp, expected=2772)

  def test_input2(self):
    inp = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
    self._invoke(inp, steps=100, expected=1940)
    self._invoke2(inp, expected=4686774924)

  #puzzle
  def test_phase1(self):
    with open(f"{self.input_loc}/day12") as inp:
      self._invoke(inp.read(), steps=1000, expected=8310)

  def test_phase2(self):
    with open(f"{self.input_loc}/day12") as inp:
      self._invoke2(inp.read(), expected=319290382980408)
