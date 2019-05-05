
class Indicator(object):
  
  def __init__(self):
    pass


class MA(Indicator):
  
  def __init__(self):
    self.value = 0
    self.date = None
    self.window_len = 0