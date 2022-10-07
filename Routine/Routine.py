from Math.Calculator import Calculator
from Math.Vector import Vector
from UI.UI import UI
from Medium import Medium

class Routine():
  @staticmethod
  def __readOmega(ui : UI):
    freq = ui.read("Input wave frequency in Hz")
    freq = float(freq)
    return Calculator.freqToOmega(freq)
  
  @staticmethod
  def __readTotalMedium(ui : UI):
    n = ui.read("Input medium amount")
    n = int(n)
    return n
  
  @staticmethod
  def __readMedium(ui : UI, n : int, omega : float):
    mediums = []
    data_name = "Medium Parameters"
    extra_info_append = ""
    parameters = Medium.param
    
    for i in range(n):
      extra_info_prepend = "{}".format(i + 1)
      param_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
      param = map(lambda x: float(x), param_str)
      mediums.append(Medium(*param, omega))
      
    return mediums
  
  @staticmethod
  def __readReflectionCoefficient(ui : UI, n : int):
    reflection = []
    inter_reflection  = []
    
    data_name = "Reflection Coefficient"
    extra_info_prepend = "in polar"
    parameters = [["mag", ""], ["angle", "in degrees"]]
    
    def readInterReflection(ui):
      extra_info_prepend = ""
      for i in range(2, n):
        extra_info_append = "at -d{}".format(i)
        coef_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
        mag, angle = map(lambda x: float(x), coef_str)
        inter_coef = Calculator.toRect(mag, angle, "degrees")
        inter_reflection.append(inter_coef)
        
    for i in range(n - 1):
      extra_info_append = "at O{}".format(i + 1)
      coef_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
      mag, angle = map(lambda x: float(x), coef_str)
      coef = Calculator.toRect(mag, angle, "degrees")
      reflection.append(coef)
      
    readInterReflection()
    
    return reflection, inter_reflection
  
  @staticmethod
  def __readIncidentWave(ui : UI):
    data_name = "Incident wave amplitude"
    extra_info_prepend = "in polar"
    extra_info_append = ""
    parameters = [["magnitude", ""], ["angle", "in degrees"]]
    
    ampl_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
    mag, ampl = map(lambda x: float(x), ampl_str)
    
    return Calculator.toRect(mag, ampl, "degrees")
  
  @staticmethod
  def __readVector(ui : UI, vector_name : str):
    data_name = "Vector {}".format(vector_name)
    parameters = [["x component", ""], ["y component", ""], ["z component", ""]]
    extra_info_prepend = ""
    extra_info_append = ""
    
    vector_component_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
    vector_component = map(lambda x: float(x), vector_component_str)
    
    return Vector(*vector_component)
  
  @staticmethod 
  def __readIncidentWavePolarized(ui : UI) -> Vector:
    return Routine.__readVector(ui, "Electric Field")
  
  @staticmethod
  def __readDirectionVector(ui : UI) -> Vector:
    return Routine.__readVector(ui, "Wave Direction")
  
  @staticmethod
  def __Mode1(ui : UI):
    n, ampl, mediums = Routine.__Mode2(ui)
    reflection, inter_reflection = Routine.__readReflectionCoefficient(ui, n)
    
    return n, ampl, mediums, reflection, inter_reflection
  
  @staticmethod
  def __Mode2(ui : UI):
    omega = Routine.__readOmega(ui)
    ampl = Routine.__readIncidentWave(ui)
    n = Routine.__readTotalMedium(ui)
    mediums = Routine.__readMedium(ui, n, omega)
    
    return n, ampl, mediums
  
  @staticmethod
  def __readBoundaryPlane(ui) -> Vector:
    data_name = "Boundary Equation"
    parameters = [["A", "x coef"], ["B", "y coef"], ["C", "z coef"]]
    extra_info_prepend = "(Ax+By+Cz = 0)"
    extra_info_append = ""
    
    plane_component_str = ui.getData(data_name, extra_info_prepend, extra_info_append, parameters)
    plane_component = map(lambda x: float(x), plane_component_str)
    
    # return the normal vector of the plane
    return Vector(*plane_component)
  
  @staticmethod
  def __Mode3(ui : UI):
    n = 2 # only support for two medium
    omega = Routine.__readOmega(ui)
    electricField = Routine.__readIncidentWavePolarized(ui)
    dir_vector = Routine.__readDirectionVector(ui)
    if ((dot := electricField.dotProduct(dir_vector)) != 0):
      message = "Expected dot product: 0. received: {}.\nElectric Field isn't orthogonal with direction vector.".format(dot)
      raise ValueError(message)
    
    mediums = Routine.__readMedium(ui, n, omega) 
    boundary_normal_vector = Routine.__readBoundaryPlane(ui)
    
    return mediums, electricField, dir_vector, boundary_normal_vector
  
  @staticmethod
  def init(ui : UI) -> list[float]:
    """Routine to read user input about data and problem type

    Returns:
        list[float]: data that are relevant in solving user defined problem
    """
    
    data = None
  
    # find type of calculation
    prompt = "Choose calculation mode below:"
    options = [
      "Find reflected and transmitted wave given reflection coef", 
      "Reflected and transmitted wave full calculation", 
      "Oblique Incidence"
      ]
    mode = ui.getOptions(prompt, options)
    
    if (mode == 1):
      data = Routine.__Mode1(ui)
      
    elif (mode == 2):
      data = Routine.__Mode2(ui)
      
    elif (mode == 3):
      data = Routine.__Mode3(ui)
      
    return mode, list(data)
  
  
  
  