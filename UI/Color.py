"""
Class for beautiful printing
using ANSI
"""
from Math.Lerp import Lerp, Kernel
from Math.Vector import Vector

class Color():
  # Class for pretty printing
  util = {
    "reset": "\u001b[0m",
    "bold": "\u001b[1m",
    "underline": "\u001b[4m",
    "reverse": "\u001b[7m",
  }
  
  color_palletes = {
    "pastel1" : [[177, 178, 255], [170, 196, 255], [210, 218, 255], [238, 241, 255]],
    "purple"  : [[147, 125, 194], [198, 137, 198], [255, 171, 255], [255, 230, 247]],
  }
  
  @staticmethod
  def generateColors(n : int, color_pallete : list[list[int]]) -> list[list[int, int, int]]:
    """Generate n colors from color pallete using bilinear filter

    Args:
        n (int): number of color that want to be generated
        color_pallete (list[list[int, int, int]]): color pallete color RGB value. 

    Returns:
        list[list[int, int, int]] : n colors from color pallete
    """
    
    colors = color_pallete
    
    # convert into a vector
    color_vector = [Vector(*color) for color in colors]
    dt = 1 / n
    t = 0
    colors = []
    for i in range(n):
      vector_color : Vector = Lerp.bilinearFilter(*color_vector, Kernel.smoothstep, round(t, 2))
      vector_color = [round(e) for e in vector_color.serialize()]
      colors.append(vector_color)
      t += dt
    
    return colors
  
  @staticmethod
  def __setFG(r, g, b):
    return f"\u001b[38;2;{r};{g};{b}m"
  
  @staticmethod
  def __setBG(r, g, b):
    return f"\u001b[48;2;{r};{g};{b}m"
  
  @classmethod
  def print_colored(cls, text: str, color_fg = None, color_bg = None, utils = None) -> str:
    """Print text with color that are specified in color_fg, color_bg, and util

    Args:
        text (str): Text that want to be printed with color
        color_fg (list[int], optional): Color of the text in RGB. Defaults to None.
        color_bg (list[int], optional): Color of the background in RGB. Defaults to None.
        util (list[str], optional): Extra params : bold, underline. Defaults to None.

    Returns:
        str: colored text
    """
    
    # add reset
    text = text + cls.util["reset"]
    
    # set fg
    if color_fg != None:
      text = cls.__setFG(*color_fg) + text
      
    # set bg
    if color_bg != None:
      text = cls.__setBG(*color_bg) + text
      
    if utils != None:
      for util in utils:
        if (x := cls.util.get(util)) != None:
          text = x + text
          
    return text 