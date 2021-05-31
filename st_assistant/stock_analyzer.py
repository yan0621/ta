class Action(object):

  def __init__(self):
    self.action = None
    self.target_id = None
    self.volume = 0


class Analyzer(object):

  def __init__(self, stock_pos_list=[], stock_prices=[], cash=0):
    self._pos_list = stock_pos_list
    self._prices = stock_prices
    self._cash = 0

  def run(self):
