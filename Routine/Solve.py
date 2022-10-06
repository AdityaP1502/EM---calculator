from re import S
from Math.Calculator import Calculator
from Medium import Medium
import cmath

class Solve():
  def __init__(self, mode, data) -> None:
    self.mode = mode
    self.data = data
    self.result = None
  # helper function
  
  
  def __setState(self, mediums : list[Medium]):
    """
    Generate value for total impedance and it's intermediate value
    """
    curr_total_impedance : float # impedance at medium center
    last_total_impedance : float # last impedance near the previous center
    
    reflection_coeff = [0 for i in range(len(mediums))]
    reflection_coef_inter = [0 for i in range(len(mediums) - 1)]
    
    # start from the n^th interface
    start = len(mediums) - 1
    
    curr_total_impedance = mediums[start].resistance
    last_total_impedance = curr_total_impedance # last impedance near the previous center
    
    for i in range(start - 1, -1, -1):
      # impedance is continuous, therefore curr_impedance = last_impedance
      # point of observation now at the center point of current medium
      curr_total_impedance = last_total_impedance
      
      # get reflective point at this point
      reflection_coeff[i] = Calculator.fromImpedanceToReflective(curr_total_impedance, mediums[i].resistance)
      
      # change the point into the intermediate point
      # intermediate point is the point near the center point of the prev medium
      
      # find reflective point at this point
      reflection_coef_inter[i - 1] = Calculator.evaluateReflective(reflection_coeff[i], 0, mediums[i].distance, mediums[i].propagation)
      
      # find its total impedance
      last_total_impedance = Calculator.fromReflectiveToImpedance(reflection_coef_inter[i - 1], mediums[i].resistance)
         
    return reflection_coeff[:-1], reflection_coef_inter[:-1]
  
  # routine
  def __solveRoutine_mode1(self):
    n, ampl, mediums, reflection, inter_reflection = self.data
    self.result = [[0, 0] for i in range(n)]
    
    self.result[0][0] = ampl
    self.result[0][1] = Calculator.getReflectionAmplitude(reflection[0], self.result[0][0])
    
    for i in range(1, n - 1):
      self.result[i][0] = Calculator.getTransmittedAmplitude(reflection[i], inter_reflection[i], mediums[i], self.result[i - 1])
      self.result[i][1] = Calculator.getReflectionAmplitude(reflection[i], self.result[i])
    
    self.result[-1][0] = self.result[-2][0] * (reflection[-1] + 1)
  
  
  def __solveRoutine_mode2(self):
    """
      given medium find all amplitude 
    """
    
    # unpack data
    n, ampl, mediums = self.data 
    reflection, inter_reflection = self.__setState(mediums)
    
    self.data.append(reflection)
    self.data.append(inter_reflection)
    
    self.__solveRoutine_mode1()
  
  def __solveRoutine_mode3():
    pass
  
  def solve(self):
    if (self.mode == 1):
      self.__solveRoutine_mode1()
      
    elif(self.mode == 2):
      self.__solveRoutine_mode2()