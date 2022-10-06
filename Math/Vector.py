from math import acos
class Vector():
  def __init__(self, x : float, y : float, z : float) -> None:
    self.x = x
    self.y = y
    self.z = z
    
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
  
  def serialize(self) -> tuple[float, float, float]:
    """Serialize vector

    Returns:
        tuple[float, float, float]: vector element in a tuple. [x, y, z]
    """
    return [self.x, self.y, self.z]
  
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
    
    return [c_x, c_y, c_z]
  
  def dotProduct(self, b : "Vector") -> float:
    """Calculate the dot product of a and b

    Args:
        b (Vector): Other vector

    Returns:
        float: a.b
    """
    
    return self.x * b.x + self.y * b.y * self.z * b.z
  
  def magnitude(self) -> float:
    """Calculate the length of the vector

    Returns:
      float : vector magnitude
    """
    
    return (self.x ** 2 + self.y ** 2 + self.z ** 2)**(0.5)
  
  def distance(self, b : "Vector") -> float:
    """Calculate the distance between of two vector

    Args:
        b (Vector): Other vector

    Returns:
        float : Distance between two vector
    """
    
    distanceVector = b - self
    return self.magnitude(distanceVector)
     
  def angle(self, b : "Vector") -> float:
    """Calculate the angle between two vector

    Args:
        b (Vector): Other vector

    Returns:
        float: angle between a and b
    """
    
    cos_theta = self.dotProduct(b) / (self.magnitude * b.magnitude)
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
    mag = a.magnitude
    
    b_x = a.magnitude / mag
    b_y = a.magnitude / mag
    b_z = a.magnitude / mag
    
    return cls(b_x, b_y, b_z)
  
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
  def changeBasis(cls, a : "Vector", new_basis : tuple["Vector", "Vector", "Vector"]) -> "Vector":
    """Change vector from ax, ay, az into a new basis vector

    Args:
        a (Vector): Vector in ax , ay , az
        new_basis (tuple["Vector"]): new basis vector
    
    Returns:
        Vector : Vector a with new basis vector
    """
    
    v1, v2, v3 = new_basis
    
    a_v1 = a.dotProduct(v1)
    a_v2 = a.dotProduct(v2)
    a_v3 = a.dotProduct(v3)
    
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
    