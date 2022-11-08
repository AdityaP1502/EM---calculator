from math import acos

from Math.Calculator import Calculator
class Vector():
  def __init__(self, x : float, y : float, z : float) -> None:
    self.x = x
    self.y = y
    self.z = z
    self.mag = self.magnitude()
    
  def __add__(self, b : "Vector"):
    c_x = self.x + b.x
    c_y = self.y + b.y
    c_z = self.z + b.z
    return Vector(c_x, c_y, c_z)
  
  def __mul__(self, k : float):
    if type(k) != type(1.1) or type(k) != type(1):
      # thrown InvalidOperationException
      NotImplemented
    
    c_x = self.x * k
    c_y = self.y * k
    c_z = self.z * k
    
    return Vector(c_x, c_y, c_z)
  
  def __sub__(self, b : "Vector"):
    return self.__add__(b * (-1))
  
  def __truediv__(self, b : float):
    return self.__mul__(1 / b)
  
  def __repr__(self) -> str:
    return "x: {}\ny:{}\nz:{}\n".format(self.x, self.y, self.z)

  def serialize(self) -> tuple[float, float, float]:
    """Serialize vector

    Returns:
        tuple[float, float, float]: vector element in a tuple. [x, y, z]
    """
    return [self.x, self.y, self.z]
  
  def serializeAngle(self, degrees: bool = False) -> list[int]:
    """Serialize vector into list of angle

    Args:
        degrees(bool). Default False: If degrees is True, the result will be in degrees else on radians. 
    
    Returns:
        list[int]: [theta_x, theta_y, theta_z]
    """
    theta_x = acos(self.x / self.mag)
    theta_y = acos(self.y / self.mag)
    theta_z = acos(self.z / self.mag)
    
    if degrees:
      theta_x, theta_y, theta_z = map(lambda x : Calculator.radToDegree(x), [theta_x, theta_y, theta_z])
      
    return [theta_x, theta_y, theta_z]

  def magnitude(self) -> float:
    """Calculate the length of the vector

    Returns:
      float : vector magnitude
    """
    
    return (self.x ** 2 + self.y ** 2 + self.z ** 2)**(0.5)
  
  def crossProduct(self, b : "Vector") -> "Vector":
    """Calculate the result of a cross b in 3D 

    Args:
        b (Vector): Other vector

    Returns:
        Vector: a x b vector
    """
    
    # Unpack the component from the tuple
    c_x = self.y * b.z - self.z * b.y
    c_y = self.z * b.x - self.x * b.z
    c_z = self.x * b.y - self.y * b.x
    
    return Vector(c_x, c_y, c_z)
  
  def dotProduct(self, b : "Vector") -> float:
    """Calculate the dot product of a and b

    Args:
        b (Vector): Other vector

    Returns:
        float: a.b
    """
    
    return self.x * b.x + self.y * b.y + self.z * b.z
  
  def distance(self, b : "Vector") -> float:
    """Calculate the distance between of two vector

    Args:
        b (Vector): Other vector

    Returns:
        float : Distance between two vector
    """
    
    distanceVector = b - self
    return distanceVector.magnitude()
     
  def angle(self, b : "Vector") -> float:
    """Calculate the angle between two vector

    Args:
        b (Vector): Other vector

    Returns:
        float: angle between a and b (in radians)
    """
    
    cos_theta = self.dotProduct(b) / (self.mag * b.mag)
    return acos(cos_theta)
  
  @classmethod
  def normalized(cls, a : "Vector") -> "Vector":
    """Find the unit vector of a vector

    Args:
        a (Vector): Vector reference

    Returns:
        Vector: unit vector of a
    """
    
    # unit vector = vector / mag
    
    return a / a.mag
  
  @staticmethod
  def inverse(M : list["Vector"]) -> list[list[float]]:
    """Calculate 3 x 3 Matrix invers

    Args:
        M (list[Vector]): 3 x 3 Matrix
        
    Returns:
        list[Vector]: 3 x 3 Inverse Matrix
     """
  
    def determinant():
      # return 3 x 3 Determinant
      return M[0].dotProduct(M[1].crossProduct(M[2]))
    
    det = determinant()
    f = (1 / det)
    
    M_float = [v.serialize() for v in M]
    temp = [0.0, 0.0, 0.0] # temp array to hold invers value
    
    Invers = []
    
    for i in range(3):
      a = (i + 1) % 3
      b = (a + 1) % 3
      
      x1 = min(a, b)
      x2 = (a + b) - x1
      
      for j in range(3):
        a = (j + 1) % 3
        b = (a + 1) % 3
        
        y1 = min(a, b)
        y2 = (a + b) - y1
        
        temp[j] = f * (M_float[x1][y1] * M_float[x2][y2] - M_float[x1][y2] * M_float[x2][y1])
        f *= -1
        
      v = Vector(*temp)
      Invers.append(v)
      
    return Invers
  
  @classmethod
  def rotate(cls, a : "Vector", angle : float, origin : tuple[float, float, float]) -> "Vector":
    """Rotate vector anngle degree about origin

    Args:
        a (Vector) : vector that want to be rotated
        angle (float): angle of rotation in degrees
        origin : rotation origin
        
    Returns:
        Vector : rotated vector a 
    """
    
    NotImplemented
    
  @classmethod
  def changeBasis(cls, a : "Vector", new_basis : list["Vector"]) -> "Vector":
    """Change vector from ax, ay, az into a new basis vector. 

    Args:
        a (Vector): Vector in ax , ay , az
        new_basis (list["Vector"]): new basis vector
    
    Returns:
        Vector : Vector a with new basis vector
    """
    
    R = cls.inverse(new_basis)
    
    a_v1 = a.x * R[0].x + a.y * R[1].x + a.z * R[2].x
    a_v2 = a.x * R[0].y + a.y * R[1].y + a.z * R[2].y
    a_v3 = a.x * R[0].z + a.y * R[1].z + a.z * R[2].z
    
    return cls(a_v1, a_v2, a_v3)
  
  @classmethod
  def revertChangeBasis(cls, a : "Vector", basis: tuple["Vector", "Vector", "Vector"]) -> "Vector":
    """Change vector basis from basis to ax, ay, az

    Args:
        a (Vector): Vector with basis vector basis
        basis (tuple["Vector"]) : basis vector of a

    Returns:
        Vector: vector with normal basis vector(ax, ay, az)
    """
    v1, v2, v3 = basis
    
    a_v1_xyz = v1 * a.x
    a_v2_xyz = v2 * a.y
    a_v3_xyz = v3 * a.z
    
    return a_v1_xyz + a_v2_xyz + a_v3_xyz
    