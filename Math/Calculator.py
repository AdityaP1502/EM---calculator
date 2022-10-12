import cmath
from math import asin, cos, degrees, pi, radians, sin, sqrt, atan


class Calculator():
  """
    Class for implementing and solving EM equations
  """
  
  # Global Constant
  e0 = 8.85 * 10 ** (-12)
  mu0 = 4 * cmath.pi * 10 ** (-7)
  
  # BASIC FUNCTION
  def freqToOmega(f: float):
    return 2 * pi * f
  
  @staticmethod
  def radToDegree(x : float):
    """Convert radian to degree

    Args:
        x (float): angle in radians

    Returns:
        float : angle in degrees
    """
    return degrees(x)
  
  @staticmethod
  def degreeToRad(x : float):
    """Convert radian to degree

    Args:
        x (float): angle in degrees

    Returns:
        float : angle in radians
    """
    return radians(x)
  
  
  @staticmethod 
  def toRect(mag : float, angle : float, angle_type: str):
    """Convert polar representation of a complex number to rectangular form

    Args:
        mag(float) : magnitude
        angle(float) : angle
        angle_type(str): radians or degrees

    Returns:
      Complex number representation in rectangular form
    """
    if (angle_type).upper() == "RADIANS":
      angle = angle
      
    elif angle_type.upper() == "DEGREES":
      angle = radians(angle)
      
    else:
      # throw UserInputErrorException
      NotImplemented
      
    # convert angle to radian
    angle = radians(angle)
    return cmath.rect(mag, angle)
  
  @staticmethod
  def toPolar(z : complex, angle_type : str):
    """Calculate polar form of a complex number

    Args:
        z (complex): Complex number in rectangular form
        angle_type(str): degrees or radians

    Returns:
        tuple[float, float] : Polar form of a complex number [mag, angle(angle_type)]
    """
    
    if angle_type.upper() == "DEGREES":
      pol = list(cmath.polar(z))
      pol[1] = Calculator.radToDegree(pol[1])
      return pol
    
    if angle_type.upper() == "RADIANS":
      return list(cmath.polar(z))
    

  # MEDIUM PARAMETER
  @staticmethod
  def calculateDistance(dist, propagation):
    # calculate distance of a medium 
    return dist * ((2 * pi) / (propagation.imag))
  
  @staticmethod
  def calculatePropagation(er, mr, sigma, omega):
    
    e = Calculator.e0 * er
    m = mr * Calculator.mu0
    
    p = sqrt(e * m / 2)
    q = sigma / (e * omega)
    
    k1 = omega * p
    k2 = sqrt(1 + q ** 2)
    
    return complex(k1 * sqrt(k2 - 1), k1 * sqrt(k2 + 1))

  @staticmethod
  def calculateResistance(er, mr, sigma, omega):
    e = Calculator.e0 * er
    m = mr * Calculator.mu0
    
    p = m / e
    q = sigma / (e * omega)
    
    mag = sqrt(p) / ((1 + q ** 2) ** (0.25))
    phase = 0.5 * atan(q)
    
    return cmath.rect(mag, phase)
  
  # Medan Bab 5 Equation Calculator
  # Impedance and Reflection Constant
  @staticmethod
  def fromImpedanceToReflective(impedance : complex, impedance_intrinsic : complex):
    return (impedance - impedance_intrinsic) / (impedance + impedance_intrinsic)
  
  @staticmethod
  def fromReflectiveToImpedance(reflective : complex, impedance_intrinsic : complex):
    f = (1 + reflective) / (1 - reflective)
    return impedance_intrinsic * f
  
  # Reflected and Transmitted Amplitude
  @staticmethod
  def evaluateReflective(curr_reflective : complex, curr_z : float, z : float, propagation_medium : complex):
    return curr_reflective * cmath.exp(-2 * propagation_medium * (z - curr_z))

  @staticmethod
  def getReflectionAmplitude(reflection, incident_amplitude):
    return reflection * incident_amplitude
  
  @staticmethod
  def getTransmittedAmplitude(reflection, inter_reflection, medium, incident_amplitude_last_medium):
    a = 1 + reflection
    b = 1 + inter_reflection
    c = (a / b) * cmath.exp(-1* medium.propagation * medium.distance) * incident_amplitude_last_medium
    return c
  
  # Medan Bab 6
  @staticmethod
  def getTransmittedAngle(incident_angle : float, medium_1_propagation : float, medium_2_propagation : float) -> float:
    if medium_2_propagation.imag < medium_1_propagation.imag:
      if incident_angle > Calculator.getCriticalAngle(medium_1_propagation, medium_2_propagation):
        # no transmitted angle exist
        return complex(0, 1)
    
    # incident angle on radian
    a = (medium_1_propagation.imag / medium_2_propagation.imag) * sin(incident_angle)
    
    # returned angle is on radian
    return asin(a)
  
  @staticmethod
  def getReflectedCoef(isNormal : bool, incident_angle : float, transmitted_angle : float, medium_1_resistance : complex, medium_2_resistance : complex):
    f = cos(transmitted_angle)
    g = cos(incident_angle)
    
    if isNormal:
      a = medium_2_resistance * g - medium_1_resistance * f
      b = medium_2_resistance * g + medium_1_resistance * f
      return a / b
    
    a = medium_2_resistance * f - medium_1_resistance * g
    b = medium_2_resistance * f + medium_1_resistance * g
    
    return -(a / b)  
  
  @staticmethod
  def getTransmittedCoef(isNormal : bool, incident_angle : float, transmitted_angle : float, medium_1_resistance : complex, medium_2_resistance : complex):
    # all angle is on radian
    f = cos(transmitted_angle)
    g = cos(incident_angle)
    
    a = 2 * medium_2_resistance * g
    
    if isNormal:
      b = medium_2_resistance * g + medium_1_resistance * f
      return a / b
    
    b = medium_2_resistance * f + medium_1_resistance * g
    return a / b
  
  @staticmethod 
  def getCriticalAngle(medium_1_propagation : float, medium_2_propagation : float):
    return asin(medium_2_propagation.imag / medium_1_propagation.imag)
  