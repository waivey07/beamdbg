def set_color(color,isBright = 0,isBackground = 0):
  colors = {
    "BLACK": 0,
    "RED": 1,
    "GREEN": 2,
    "YELLOW": 3,
    "BLUE": 4,
    "MAGENTA": 5,
    "CYAN": 6,
    "WHITE": 7
  }  
  basecode = 30
  magic = "\033[{}m"
  backgroundcode = 10
  brightcode = 60
  result = 0
  if color == 0:
    return magic.format("0")
  result = colors.get(color.upper(), None)+basecode
  if isBackground:
    result += backgroundcode
  if isBright:
    result += brightcode
  result = magic.format(result)
  return result