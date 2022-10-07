from Math.Calculator import Calculator
class Medium():
  param = [["er", "Relative Permitivity"], ["mr", "Relative Permeability"], ["sigma", "Conductivity (for perfect conductor insert infinity)"], ["distance", "(on lambda) : Ex. 0.1 => 0.1 * lambda. 0 if on the edge"]]
  def __init__(self, er, mr, sigma, dist, omega) -> None:
    self.propagation = Calculator.calculatePropagation(er, mr, sigma, omega) 
    self.resistance = Calculator.calculateResistance(er, mr, sigma, omega)
    # logger
    # print("Nilai propagasi: {}".format(self.propagation))
    # print("Nilai impedansi: {}".format(self.resistance))
    self.distance = Calculator.calculateDistance(dist, self.propagation)

  