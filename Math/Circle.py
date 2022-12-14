from Math.Vector import Vector

PRECISION = 5

class Circle():
  def __init__(self, x_center : float, y_center : float, r : float) -> None:
    self.center = Vector(x_center, y_center, 0)
    self.radius = r
  
  @staticmethod
  def intersection(a : "Circle", b : "Circle") -> list[Vector]:
    length = a.center.distance(b.center)
    min_rad = min(a.radius, b.radius)
    max_rad = max(a.radius, b.radius)
    if (length > a.radius + b.radius): return []
    if (length < max_rad - min_rad and length + min_rad < max_rad): return []
    if (length == a.radius + b.radius):
      return a.center * 2
    
    dist = b.center - a.center
    x = (length ** 2 - (b.radius ** 2 - a.radius ** 2)) / (2 * length)
    h = (a.radius ** 2 - x ** 2) ** (0.5)
    
    intersect_x1 = round((x * dist.x - h * dist.y) / length, PRECISION)
    intersect_y1 = round((h * dist.x + x * dist.y) / length, PRECISION)
    
    intersect_x2 = round((x * dist.x + h * dist.y) / length, PRECISION)
    intersect_y2 = round((-h * dist.x + x * dist.y) / length, PRECISION)
    
    return [a.center + Vector(intersect_x1, intersect_y1, 0),a.center + Vector(intersect_x2, intersect_y2, 0)]
  
  @staticmethod
  def findReflectiveFromImpedanceNormalized(Zl : complex):
    # find reflective from zn_c
    r_real_circle = 1 / (Zl.real + 1)
    r_imag_circle = 1 / Zl.imag
    
    real_circle = Circle(Zl.real * r_real_circle, 0, abs(r_real_circle))
    imag_circle = Circle(1, r_imag_circle, abs(r_imag_circle))
    
    reflective_zn = [vec for vec in Circle.intersection(real_circle, imag_circle) if (int(vec.x) == 1 and int(vec.y) != 0 or int(vec.x) != 1)]
    
    if (len(reflective_zn) == 0): 
      raise Exception("Cannot find intersection")
    
    reflective_zn = reflective_zn[0]
    return reflective_zn

if __name__ == "__main__":
  a = Circle(0, 0, 1)
  b = Circle(1, 1, 2)
  print(Circle.intersection(a, b))