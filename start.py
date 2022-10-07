from Math.Calculator import Calculator
from Routine.Routine import Routine
from Routine.Solve import Solve
from UI.UI import UI, Color
# User inteface and main files

if __name__ == "__main__":
  mode, data = None, None
  try:
    mode, data = Routine.init()
  except ValueError as e:
    print("Oops...Something is wrong when init calculation.")
    print(e)
    print("Exiting!")
    exit(-1)
    
  solver = Solve(mode, data)
  solver.solve()
  result = solver.result
  
  