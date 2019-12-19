import unittest
import os

class TestDay(unittest.TestCase):
  def setUp(self):
    testdir = os.path.dirname(__file__)
    inp_path = 'inputs'
    self.input_loc = os.path.join(testdir, inp_path)
  
