from os import system
from UI.Color import Color

class UI(Color):
  def __init__(self, color_pallete : str) -> None:
    super().__init__()
    self.themes = self.color_palletes.get(color_pallete, None)
    if self.themes == None:
      raise Exception("Unrecognized Themes")
  
  def showOptions(self, prompt : str, options : list[str]) -> None:
    """Show options in a given format
    " prompt :
      1. options[0]
      2. options[1]
      3. options[2]
      .
      .
      .
    "
    
    Args:
        prompt (str): prompt string
        options (list[str]): option string 
    """
    
    option_format = "{} :\n".format(prompt)
    
    options = ["{}. {}".format(i + 1, v) for i, v in enumerate(options)]
    options_string = "\n".join(options)
    
    option_format += options_string
    print(option_format)
  

  def getOptions(self, prompt : str, options : list[str]) -> int:
    """Read user option

    Args:
        n_max (int): number of options available

    Returns:
      int: user options  
    """
    
    # print options
    self.showOptions(prompt, options)
    n_max = len(options)
    
    # read input
    user_option = int(input("Masukkan option:\n>"))
    if user_option < 1 or user_option > n_max:
      message = "Invalid Option. Expected value range: [1, {}], received: {}. \nInput option must be between 1 and {}. ".format(n_max, user_option, n_max)
      raise ValueError(message)

    return user_option
  
  def __dataFormatString(self, data_name : str, extra_info_prepend : str, extra_info_append : str, data_parameters : list[str, str], colors : list[list[int]]) -> str:
    """ Generate prompt when inputting data with format
        " Masukkan bold({data_name} {extra_info_prepend}) (color_1(parameter_1) + extra_info_param_1 + ...) + extra_info_append
          bold, underline(Please put space in between parameters!)
          >
        " 
    Args:
        data_name (str): data name
        extra_info_prepend: info that want to be put before parameter
        extra_info_append: info that want to be put after parameter
        data_parameters (list[str, str]): list consist of parameter name and extra info about the input
        colors (default : None): parameter color RGB value. 
    Returns:
        str: input string
    """
    
    parameter_str = [" ".join([(self.print_colored(name, color_fg=colors[i])), info]) for (i, (name, info)) in enumerate(data_parameters)]
    parameter_str = ", ".join(parameter_str)
    
    prefix = "Masukkan " + self.print_colored(data_name, utils=["bold"]) + " " + extra_info_prepend +"("
    suffix = ") {} \n{}".format(extra_info_append, self.print_colored("Please put space between parameter", utils=["bold", "underline"]))
    return prefix + parameter_str + suffix
    
  def getData(self, data_name : str, extra_info_prepend : str, extra_info_append : str, data_parameters : list[str, str], colors : list[list[int]] = None) -> list[str]:
    """Get data with prompt with specified format

   Args:
        data_name (str): data name
        extra_info_prepend: info that want to be put before parameter
        extra_info_append: info that want to be put after parameter
        data_parameters (list[str, str]): list consist of parameter name and extra info about the input
        colors(default : None): parameter color RGB value. If not specified, will use from color pallete
        
    Returns:
        list[str] : parameter data
    """
    if colors == None:
      colors = self.generateColors(len(data_parameters), self.themes)
    
    print(colors)
    input_prompt = self.__dataFormatString(data_name, extra_info_prepend, extra_info_append, data_parameters, colors)
    print(input_prompt)
    
    parameter = input("Please input the parameter:\n>").split(" ")
    return parameter
  
  @staticmethod
  def read(prompt : str) -> str:
    """Read user input for a given prompt. Only take one value as data. 

    Args:
        prompt (str): Prompt

    Returns:
        str: user input
    """
    
    return input(prompt + "\n>")
  
def showResult():
  pass
