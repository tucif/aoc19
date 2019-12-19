import unittest
from io import StringIO

from test.lib import TestDay

from day2 import intcode
from day2 import Program
from day2 import find_result


class TestDay2(TestDay):

  # Samples
  def test_sum(self):
    code = '1,0,0,0,99'
    program = Program(code)
    intcode(program)
    # Test 1+1, stored at pos 0
    self.assertEqual(program.code[0], 2)

  def test_mul(self):
    program = Program('2,3,0,3,99')
    intcode(program) 
    # Test 3*2, stored at pos 3
    self.assertEqual(program.code[3], 6)

  def test_mul2(self):
    program = Program('2,4,4,5,99,0')
    intcode(program)
    # Test 99*99 = 9801 at pos 5
    self.assertEqual(program.code[5], 9801)

  def test_sum_mul(self):
    program = Program('1,1,1,4,99,5,6,0,99')
    intcode(program)
    # Test 1+1 into pos 4, which makes 5*6 into pos 0
    self.assertEqual(program.code[0], 30)

  # 
  # Puzzles
  #
  def test_phase1(self):
    with open(f'{self.input_loc}/day2') as inp:
      program = Program(inp.read())
      program.code[1] = 12
      program.code[2] = 2
      intcode(program)
      self.assertEqual(program.code[0], 6327510)

  def test_phase2(self):
    with open(f'{self.input_loc}/day2') as inp:
      program = Program(inp.read())
      target = 19690720
      answer = find_result(target, program.code)
      self.assertEqual(answer, 4112)
    
from day2 import standalone
class TestDay5(TestDay):

  # Samples
  def test_immediate_mul(self):
    program = Program('1002,4,3,4,33')
    intcode(program)
    # 33 * 3 stored at pos 4
    self.assertEqual(program.code[4], 99)

  def test_negative(self):
    program = Program('1101,100,-1,4,0')
    intcode(program)
    # Test 100+ -1 at pos 4
    self.assertEqual(program.code[4], 99)

  def test_eq_pos(self):
    code = '3,9,8,9,10,9,4,9,99,-1,8'
    program = Program(code)
    # output is 1 if input equals 8 else 0
    output = StringIO()
    standalone(program, '8', output)
    self.assertEqual(output.read().rstrip(), '1')

    program = Program(code)
    output = StringIO()
    standalone(program, '7', output)
    self.assertEqual(output.read().rstrip(), '0')

  def test_lt_pos(self):
    code = '3,9,7,9,10,9,4,9,99,-1,8'
    program = Program(code)
    # output is 1 if input is less than 8 else 0
    output = StringIO()
    standalone(program, '7', output)
    self.assertEqual(output.read().rstrip(), '1')

    program = Program(code)
    output = StringIO()
    standalone(program, '9', output)
    self.assertEqual(output.read().rstrip(), '0')

  def test_eq_imm(self):
    code = '3,3,1108,-1,8,3,4,3,99'
    program = Program(code)
    # output is 1 if input equals 8 else 0
    output = StringIO()
    standalone(program, '8', output)
    self.assertEqual(output.read().rstrip(), '1')

    program = Program(code)
    output = StringIO()
    standalone(program, '88', output)
    self.assertEqual(output.read().rstrip(), '0')

  def test_lt_imm(self):
    code = '3,3,1107,-1,8,3,4,3,99'
    program = Program(code)
    # output is 1 if input is less than 8 else 0
    output = StringIO()
    standalone(program, '1', output)
    self.assertEqual(output.read().rstrip(), '1')
    
    program = Program(code)
    output = StringIO()
    standalone(program, '9', output)
    self.assertEqual(output.read().rstrip(), '0')


  def test_jmp_pos(self):
    code = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    program = Program(code)
    # output 0 if input is zero else 1
    output = StringIO()
    standalone(program, '0', output)
    self.assertEqual(output.read().rstrip(), '0')

    program = Program(code)
    output = StringIO()
    standalone(program, '2', output)
    self.assertEqual(output.read().rstrip(), '1')

  def test_jmp_imm(self):
    code = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    program = Program(code)
    # output 0 if input is zero else 1
    output = StringIO()
    standalone(program, '0', output)
    self.assertEqual(output.read().rstrip(), '0')

    program = Program(code)
    output = StringIO()
    standalone(program, '2', output)
    self.assertEqual(output.read().rstrip(), '1')

  def test_lt_qe_gt(self):
    code = ('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
           '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
           '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')
    # 999 if value < 8
    program = Program(code)
    output = StringIO()
    standalone(program, '0', output)
    self.assertEqual(output.read().rstrip(), '999')

    # 1000 if value == 8
    program = Program(code)
    output = StringIO()
    standalone(program, '8', output)
    self.assertEqual(output.read().rstrip(), '1000')

    # 1001 if value > 8
    program = Program(code)
    output = StringIO()
    standalone(program, '80', output)
    self.assertEqual(output.read().rstrip(), '1001')


  # Puzzles
  def test_phase1(self):
    with open(f'{self.input_loc}/day5') as inp:
      program = Program(inp.read())
      output = StringIO()
      standalone(program, '1', output)
      self.assertEqual(output.read().rstrip(), '10987514')

  def test_phase2(self):
    with open(f'{self.input_loc}/day5') as inp:
      program = Program(inp.read())
      output = StringIO()
      standalone(program, '5', output)
      self.assertEqual(output.read().rstrip(), '14195011')
    


class TestDay9(TestDay):

  # Samples
  def test_quine(self):
    code = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    program = Program(code, rw=False)
    output = StringIO()
    # no rewind output every call to read it in full at the end
    standalone(program, '', output)
    quine = ','.join(output.read().rstrip().split('\n'))
    # Program should output a copy of itself
    self.assertEqual(quine, code)


  def test_16d(self):
    code = '1102,34915192,34915192,7,4,7,99,0'
    program = Program(code)
    output = StringIO()
    standalone(program, '', output)
    # should output 16 digit number
    self.assertEqual(len(output.read().rstrip()), 16)


  def test_largenum(self):
    code = '104,1125899906842624,99'
    program = Program(code)
    output = StringIO()
    standalone(program, '', output)
    # should output the large number from code[1]
    self.assertEqual(output.read().rstrip(), code.split(',')[1])


  # Puzzles
  def test_phase1(self):
    with open(f'{self.input_loc}/day9') as inp:
      program = Program(inp.read())
      output = StringIO()
      standalone(program, '1', output)
      self.assertEqual(output.read().rstrip(), '2870072642')

  def test_phase2(self):
    with open(f'{self.input_loc}/day9') as inp:
      program = Program(inp.read())
      output = StringIO()
      standalone(program, '2', output)
      self.assertEqual(output.read().rstrip(), '58534')


from day7 import evaluate_amplifiers
class TestDay7(TestDay):

  # Samples
  # Amplifier Phases 0-4
  def test_43210(self):
    program = Program('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    max_signal = evaluate_amplifiers(program, min_phase=0, max_phase=4)
    self.assertEqual(max_signal, 43210)

  def test_54321(self):
    program = Program('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    max_signal = evaluate_amplifiers(program, min_phase=0, max_phase=4)
    self.assertEqual(max_signal, 54321)

  def test_65210(self):
    program = Program('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,'
                      '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    max_signal = evaluate_amplifiers(program, min_phase=0, max_phase=4)
    self.assertEqual(max_signal, 65210)


  # Amplifier Phases 5-9
  def test_139629729(self):
    program = Program('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,'
                      '1001,28,-1,28,1005,28,6,99,0,0,5')
    max_signal = evaluate_amplifiers(program, min_phase=5, max_phase=9)
    self.assertEqual(max_signal, 139629729)

  def test_18216(self):
    program = Program('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,'
                      '26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,'
                      '55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
    max_signal = evaluate_amplifiers(program, min_phase=5, max_phase=9)
    self.assertEqual(max_signal, 18216)

  # Puzzles
  def test_phase1(self):
    with open(f'{self.input_loc}/day7') as inp:
      program = Program(inp.read())
      max_signal = evaluate_amplifiers(program, min_phase=0, max_phase=4)
      self.assertEqual(max_signal, 87138)

  def test_phase2(self):
    with open(f'{self.input_loc}/day7') as inp:
      program = Program(inp.read())
      max_signal = evaluate_amplifiers(program, min_phase=5, max_phase=9)
      self.assertEqual(max_signal, 17279674)
      

from day11 import hull_painting
from day11 import render_panels
class TestDay11(TestDay):
  def test_phase1(self):
    with open(f'{self.input_loc}/day11') as inp:
      program = Program(inp.read())
      (painted,x,y) = hull_painting(program, 0)
      self.assertEqual(len(painted), 1785)

  def test_phase2(self):
    expected = '''
                                           #  #   ##  ##  #      ## #### #### #  #  
                                           #  #    # #  # #       #    # #    #  #  
                                           ####    # #  # #       #   #  ###  ####  
                                           #  #    # #### #       #  #   #    #  #  
                                           #  # #  # #  # #    #  # #    #    #  #  
                                           #  #  ##  #  # ####  ##  #### #    #  # '''
    with open(f'{self.input_loc}/day11') as inp:
      program = Program(inp.read())
      (painted,x,y) = hull_painting(program, 1)
      render = render_panels(painted, x, y)
      self.assertTrue(expected in render)
