from Math.Calculator import Calculator
from Routine.Init import Init
from Routine.Solve import Solve
from UI.UI import UI, Color
# User inteface and main files


# class Read():
#   @staticmethod
#   def routine():
#     print("""Masukkan mode kalkulasi:
#              1. Kalkulasi Amplituda tiap interface(diketahui koefisien refleksi)
#              2. Full calculation(Hanya diberikan data medium)""")
#     try:
#       mode = int(input(">"))
#     except ValueError as e:
#       print("Ada yang salah pada mode yang diinput. Harap masukkan integer")
#       exit(-1)
      
#     if (mode < 1 or mode > 2):
#       print("Masukkan tidak sesuai. Harap masukkan opsi yang benar")
#       exit(-1)
       
#     print("Pilih (0) jika merambat ke kanan dan pilih (1) jika merambat ke kiri")
#     try:
#       isLeft = int(input(">"))
#     except ValueError as e:
#       print("Ada yang salah pada mode yang diinput. Harap masukkan integer")
#       exit(-1)
      
#     if (isLeft < 0 or isLeft > 1):
#       print("Masukkan tidak sesuai. Harap masukkan opsi yang benar")
#       exit(-1)
      
#     n = int(input("Masukkan jumlah medium yang ada:\n>"))
#     print(Color.print_colored("Notes:", utils=["bold"]) + "Tiap input dimasukkan dalam bentuk polar")
#     print("Masukkan amplituda incident wave.")
#     ampl, omega = Read.readIncidentWavePolar()
#     print("Masukkan parameter medium")
#     mediums = Read.readMedium(n, omega)
#     if (isLeft == 1):
#       # change distance into negative
#       for medium in mediums:
#         medium.distance = -medium.distance
    
#     if (mode == 1):
#       print("Masukkan koefisien refleksi ")
#       reflection, inter_reflection = Read.readTotalReflectectionPolar(n)
      
#     if (mode == 2):
#       print(Color.print_colored("Melakukan kalkulasi!", utils=["bold", "underline"]))
#       reflection, inter_reflection = Solve.setState(mediums)
#       print("Done!")
#       for i in range(len(reflection)):
#         print("Koefisien refleksi di medium {}: {}".format(i + 1, reflection[i]))
#         pol = list(cmath.polar(reflection[i]))
#         pol[1] = degrees(pol[1])
#         print("Dalam polar: {}<{}".format(*pol))
#       for i in range(len(inter_reflection)):
#         print("Koefisien refleksi di titik -d{}: {}".format(i + 2, inter_reflection[i]))
#         pol = list(cmath.polar(inter_reflection[i]))
#         pol[1] = degrees(pol[1])
#         print("Dalam polar: {}<{}".format(*pol))

#     return n, ampl, mediums, reflection, inter_reflection


if __name__ == "__main__":
  mode, data = None, None
  try:
    mode, data = Init.init()
  except ValueError as e:
    print("Oops...Something is wrong when init calculation.")
    print(e)
    print("Exiting!")
    exit(-1)
    
  
  solver = Solve(mode, data)
  solver.solve()
  result = solver.result
  
  # need to use UI class to show result
  # just to unit test the program
  for i in range(len(result)):
      print("Em{}+: {}".format(i + 1, result[i][0]))
      pol = Calculator.toPolar(result[i][0], "degrees")
      print("Dalam polar: {}<{}".format(*pol))
      print("Em{}-: {}".format(i + 1, result[i][1]))
      pol = Calculator.toPolar(result[i][1], "degrees")
      print("Dalam polar: {}<{}".format(*pol))
  