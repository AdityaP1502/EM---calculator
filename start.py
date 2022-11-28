from Routine.Routine import Routine
from Routine.Solve import Solve
from UI.UI import UI
# User inteface and main files

if __name__ == "__main__":
  mode, data = None, None
  # create UI instance
  ui = UI(color_pallete="purple")
  
  try:
    mode, data = Routine.init(ui)
  except Exception as e:
    print("Oops...Something is wrong when init calculation.")
    print(e)
    print("Exiting!")
    exit(-1)
    
  solver = Solve(mode, data, ui)
  solver.solve()
  result = solver.result
  