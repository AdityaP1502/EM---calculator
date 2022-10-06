from Math.Calculator import Calculator
from UI.UI import UI
from Medium import Medium

class Init():
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
  def __readIncidentWavePolarized():
    pass
  
  @staticmethod
  def __readDirectionVector():
    pass
  
  @staticmethod
  def __Mode1(ui : UI):
    n, ampl, mediums = Init.__Mode2(ui)
    reflection, inter_reflection = Init.__readReflectionCoefficient(ui, n)
    
    return n, ampl, mediums, reflection, inter_reflection
  
  @staticmethod
  def __Mode2(ui : UI):
    omega = Init.__readOmega(ui)
    ampl = Init.__readIncidentWave(ui)
    n = Init.__readTotalMedium(ui)
    mediums = Init.__readMedium(ui, n, omega)
    
    return n, ampl, mediums
  
  @staticmethod
  def __Mode3():
    pass
  
  @staticmethod
  def init() -> list[float]:
    """Routine to read user input about data and problem type

    Returns:
        list[float]: data that are relevant in solving user defined problem
    """
    
    data = None
    
    # create UI instance
    ui = UI(color_pallete="purple")

    # find type of calculation
    prompt = "Choose calculation mode below:"
    options = ["Find reflected and transmitted wave given reflection coef", "reflected and transmitted wave full calculation"]
    mode = ui.getOptions(prompt, options)
    
    if (mode == 1):
      data = Init.__Mode1(ui)
      
    elif (mode == 2):
      data = Init.__Mode2(ui)
      
      
    return mode, list(data)
  
  
  
  