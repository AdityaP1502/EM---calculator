from math import cos, sin
from Math.Calculator import Calculator
from Math.Vector import Vector
from Math.Circle import Circle
from Medium import Medium
from UI.UI import UI
class Solve():
  def __init__(self, mode : int, data : any, ui : UI) -> None:
    self.mode = mode
    self.data = data
    self.result = None
    self.log = ui
    
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
      self.result[i][0] = Calculator.getTransmittedAmplitude(reflection[i - 1], inter_reflection[i - 1], mediums[i].propagation, mediums[i].distance, self.result[i - 1][0])
      self.result[i][1] = Calculator.getReflectionAmplitude(reflection[i], self.result[i][0])
    
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
  
  def __solveRoutine_mode3(self):
    def findReflectedWave():
      # tangential set component at v3 = 0
      
      # reflected coefficient
      if (type(transmittedAngle) == complex):
        coefTangential = 1
        coefNormal = -1
      else:
        medium_resistances = [x.resistance for x in mediums]
        coefTangential = Calculator.getReflectedCoef(False, incidentAngle, transmittedAngle, *medium_resistances)
        coefNormal = Calculator.getReflectedCoef(True, incidentAngle, transmittedAngle, *medium_resistances)
      
      # find direction vector reflected
      # flip the component in v1 
      dirVectorNew = dirVector * 1
      dirVectorNew.x *= -1
      
      # find reflected electric field
      # reflected e field direction only has v2 component flipped for tangential
      reflectedWaveTangential = electricFieldTangential * coefTangential
      reflectedWaveTangential.y *= -1
      
      # normal just scale with the coef
      reflectedWaveNormal = electricFieldNormal * coefNormal
      
      return reflectedWaveTangential + reflectedWaveNormal, dirVectorNew
    
    def findTransmittedWave():
      if (type(transmittedAngle) == complex):
        return Vector(0, 0, 0), Vector(0, 0, 0)

      medium_resistances = [x.resistance for x in mediums]
      coefTangential = Calculator.getTransmittedCoef(False, incidentAngle, transmittedAngle, *medium_resistances)
      coefNormal = Calculator.getTransmittedCoef(True, incidentAngle, transmittedAngle, *medium_resistances)
      
      # direction vector has the same mag just different direction
      signX = -1 if dirVector.x < 1 else 1
      signY = -1 if dirVector.y < 1 else 1
      
      dx = dirVector.mag * signX * cos(transmittedAngle)
      dy = dirVector.mag * signY * sin(transmittedAngle)
      dz = 0
      # create a new vector instance
      dirVectorNew = Vector(dx, dy, dz)
      
      # Electric field has the same direction just different amplitude
      transmittedWaveTangential = electricFieldTangential * coefTangential
      transmittedWaveNormal = electricFieldNormal * coefNormal
      
      return transmittedWaveTangential + transmittedWaveNormal, dirVectorNew
         
    # type hint
    mediums : list[Medium]
    electricField : Vector
    dirVector : Vector
    boundaryNormalVector : Vector
    
    # unpack the data
    mediums, electricField, dirVector, boundaryNormalVector = self.data
    
    # find POI
    POINormalVector = Vector.normalized(dirVector.crossProduct(boundaryNormalVector))
    
    # Shift Coordinate
    # NEW BASIS VECTOR
    v1 = Vector.normalized(boundaryNormalVector) # tangential 
    v2 = POINormalVector.crossProduct(v1) # tangential
    v3 = POINormalVector # normal
    
    # Convert E in ax, ay, az into new basis vector v1, v2, v3
    electriFieldNew = Vector.changeBasis(electricField, [v1, v2, v3])
    
    # find incident angle and transmitted angle
    # incident angle is the angle between dir vector and v1
    incidentAngle = dirVector.angle(v1) # in radians
    medium_propagations = [x.propagation for x in mediums]
    transmittedAngle = Calculator.getTransmittedAngle(incidentAngle, *medium_propagations)
    
    # find tangential component and normal component
    electricFieldTangential = electriFieldNew * 1 # copy the vector       
    electricFieldTangential.z = 0
      
    # normal component set v1 = 0 and v2 = 0
    electricFieldNormal = electriFieldNew * 1 # copy the vector
    electricFieldNormal.x = 0; electricFieldNormal.y = 0
    
    # do calculation using new vector
    # Calculation
    reflectedWave = findReflectedWave()
    transmittedWave = findTransmittedWave()
    
    # revert all vector back to ax, ay and az
    vectors = [reflectedWave, transmittedWave]
    self.result =  [
      [Vector.revertChangeBasis(p, [v1, v2, v3]), Vector.revertChangeBasis(q, [v1, v2, v3])] 
      for (p, q) in vectors
    ] 
  
  def __solveRoutine_mode5(self):
    mode, impedance = self.data 
    loc_stub = 0.25
    
    init_point = impedance
    
    # Calculate stub distance in SC mode
    # matching circle
    
    reflective_zn = Circle.findReflectiveFromImpedanceNormalized(init_point)
    
    if (mode == "PARALEL"):
      complex_reflective_zn = complex(reflective_zn.x, reflective_zn.y)
      complex_reflective_zn = Calculator.rotateComplex(complex_reflective_zn, 0.25, True)
      
      reflective_zn.x = complex_reflective_zn.real
      reflective_zn.y = complex_reflective_zn.imag
      
      loc_stub = 0
      
    r = reflective_zn.mag
    
    distance = [] # in lambda
    matching_circle = Circle(0.5, 0, 0.5)
    
    search_circle = Circle(0, 0, r)
    zb = Circle.intersection(matching_circle, search_circle)
    
    if (len(zb) == 0): raise Exception("Can't find points, because matching cirle doesn't intersect with load")
    
    for i in range(len(zb)):
      reflective = complex(zb[i].x, zb[i].y)
      _, angle = Calculator.toPolar(reflective, "DEGREES")
      if angle < 0:
        angle = 180 - angle
      
      loc1 = angle / 720
      
      impedance = Calculator.fromReflectiveToImpedanceNormalized(reflective)
      stub = 1 - impedance
      reflective = Calculator.imaginaryImpedanceToReflective(stub)
      
      # Calculate distance
      _, angle = Calculator.toPolar(reflective, "DEGREES")
      if angle < 0:
        angle = 180 - angle
      loc2 = angle / 720
      
      distance_stub = Calculator.calculateTransmissionDistance(loc_stub, loc2)
      distance_load =  Calculator.calculateTransmissionDistance(loc1, loc_stub)
      distance.append([impedance, distance_stub, distance_load])
    
    self.result = distance

  def __solveRoutine_mode6(self):
    Zl, freq_sample, dist, L, C = self.data
    res = []
    
    for freq in freq_sample:
      beta = Calculator.transmissionLineBeta(freq, L, C)
      dl = Calculator.getDistanceInLambda(dist, beta)
      reflective_zn = Circle.findReflectiveFromImpedanceNormalized(Zl)
      
      complex_reflective_zn  = complex(reflective_zn.x, reflective_zn.y)
      complex_reflective_zn = Calculator.rotateComplex(complex_reflective_zn, dl, True)
      
      Zb = Calculator.fromReflectiveToImpedanceNormalized(complex_reflective_zn)
      alpha = Zb.real
      swr = Calculator.SWR(alpha)
      
      res.append((freq, swr))
    
    self.result = res
      
  def __getResult_mode2(self):
    # type hint
    self.result : list[list[Vector]]
    
    for (i, (ampl, reflected_ampl)) in enumerate(self.result):
      self.log.showResult(data_name="Electric field at medium {} (Em{}+)".format(i + 1, i + 1), values=ampl)
      self.log.showResult(data_name="Electric field at medium {} (Em{}+) in polar form(mag, angle)".format(i + 1, i + 1), values=Calculator.toPolar(ampl, "DEGREES"))
      self.log.showResult(data_name="Reflected Electric field at medium {} (Em{}-)".format(i + 1, i + 1), values=reflected_ampl)
      self.log.showResult(data_name="Reflected Electric field at medium {} (Em{}-) in polar form(mag, angle)".format(i + 1, i + 1), values=Calculator.toPolar(reflected_ampl, "DEGREES"))
      
  def __getResult_mode3(self):
    # type hint 
    self.result : list[list[Vector]]
    
    self.log.showResult(data_name="Reflected electric field vector", values=self.result[0][0].serialize())
    self.log.showResult(data_name="Reflected wave direction vector", values=self.result[0][1].serialize())
    self.log.showResult(data_name="Transmitted electric field vector", values=self.result[1][0].serialize())
    self.log.showResult(data_name="Transmitted wave direction vector", values=self.result[1][1].serialize())
    
  def __getResult_mode4(self):
    self.result : list[Medium] = self.data
    for (i, medium) in enumerate(self.result):
      self.log.showResult(data_name="Medium Propagation at {}".format(i + 1), values=medium.propagation)
      self.log.showResult(data_name="Medium Propagation at {}(polar)".format(i + 1), values=Calculator.toPolar(medium.propagation, "DEGREES"))
      self.log.showResult(data_name="Resisatnce at {}".format(i + 1), values=medium.resistance)
      self.log.showResult(data_name="Resisatnce at {}(polar)".format(i + 1), values=Calculator.toPolar(medium.resistance, "DEGREES"))
  
  def __getResult_mode5(self):
    for i in range(len(self.result)):
      self.log.showResult(data_name="ds (point: {})".format(self.result[i][0]), values=self.result[i][1])
      self.log.showResult(data_name="dl (point: {})".format(self.result[i][0]), values=self.result[i][2])
  
  def __getResult_mode6(self):
    content = "freq(Hz),SWR\n"
    content_str = [("{},{}").format(freq, swr) for freq, swr in self.result]
    content_str = "\n".join(content_str)
    content += content_str
      
    # save data to csv
    with open("swr.csv", "w") as f:
      f.write(content)
    
      
  def solve(self):
    if (self.mode == 1):
      self.__solveRoutine_mode1()
      
    elif(self.mode == 2):
      self.__solveRoutine_mode2()
      self.__getResult_mode2()
      
    elif self.mode == 3:
      self.__solveRoutine_mode3()
      self.__getResult_mode3()
      
    elif self.mode == 4:
      self.__getResult_mode4()
      
    elif self.mode == 5:
      self.__solveRoutine_mode5()
      self.__getResult_mode5()
      
    elif self.mode == 6:
      self.__solveRoutine_mode6()
      self.__getResult_mode6()
      