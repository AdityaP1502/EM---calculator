from Math.Vector import Vector
class Kernel():
  """Lerp function kernel
  """
  @staticmethod
  def linear(t : float) -> float: 
    """Linear kernel

    Args:
        t (float): time. between 0 and 1

    Returns:
        float : result
    """
    return t
  
  @staticmethod
  def squared(t : float) -> float: 
    """Square kernel

    Args:
        t (float): time

    Returns:
        float: result
    """
    return t * t
  
  @staticmethod
  def smoothstep(t : float) -> float: 
    """Smoothstep kernel. Combination of slow start and slow finish

    Args:
        t (float): time

    Returns:
        float: result
    """
    v1 = t * t
    v2 = 1 - (1 - t) * (1 - t)
    return Lerp.lerp(v1, v2, Kernel.linear, t)
  
  @staticmethod
  def parabola(k : float) -> "function":
    """Generate parabola function with specified k

    Args:
        k (float): parabola sharpness

    Returns:
        function: parabola function with defined sharpness
    """
    def func(t : float) -> float:
      """Parabole kernel

      Args:
          t (float): time. Between 0 and 1

      Returns:
          float: result
      """
      return (4 * t * (1 - t)) ** k
    return func 
  
  @staticmethod
  def triangle(t : float) -> float:
    """triangle kernel

    Args:
        t (float): time. between 0 and 1

    Returns:
        float: result
    """
    return 1 - 2 * abs(t - 0.5)
  
  @staticmethod
  def bounce_out(t : float) -> float:
    """bounce out kernel. after reach the end will bounce and oscillate

    Args:
        t (float): time

    Returns:
        float: result
    """
    
    # MAGIC NUMBER
    n1 = 7.5625
    d1 = 2.75
    
    if (t < 1 / d1):
      return n1 * t * t
    
    elif (t < 2 / d1):
      t = 1.5 / d1
      return n1 * t * t + 0.75
    
    elif (t < 2.5 / d1):
      t = 2.25 / d1
      return n1 * t * t + 0.9375
    
    else:
      t = 2.625 / d1
      return n1 * t * t + 0.984375
    
class Lerp():
  """Linear interpolation
  """
  @staticmethod
  def lerp(A : Vector, B : Vector, f : "function", t : float) -> Vector:
    """Linear interpolation from A to B

    Args:
        A (Vector): Start Position Vector
        B (Vector): End Position Vector
        f (function): Lerp kernel function. Defined in Kernel class
        t (float): time, 0 <= t <= 1

    Returns:
        Vector: linear interpolation at time = t
    """
    
    constant = f(t)
    A_multi = 1 - constant
    B_multi  = constant
    
    return A * A_multi + B * B_multi
  
  @staticmethod
  def bilinearFilter(A : Vector, B : Vector, C : Vector, D : Vector, f : "function", t : float) -> Vector:
    """Bilinear filter

    Args:
        A (Vector): Vector 1.1
        B (Vector): Vector 1.2
        C (Vector): Vector 2.1
        D (Vector): Vector 2.2
        f (function): Kernel
        t (float) : time

    Returns:
        Vector: Bilinear interpolation point at time = t
    """
    
    v1 = Lerp.lerp(A, B, f, t)
    v2 = Lerp.lerp(C, D, f, t)
    
    return Lerp.lerp(v1, v2, f, t)
  
  

    