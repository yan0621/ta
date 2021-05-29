class StockPrice(object):

  def __init__(self, stock_id, name, start, last_end, current, high, low):
    self.id = stock_id
    self.name = name
    self.start = start
    self.last_end = last_end
    self.current = current
    self.high = high
    self.low = low

  def __str__(self):
    return "{%s, %s, start=%f, last_end=%f, current=%f, high=%f, low=%f}" % (self.id, self.name, self.start, self.last_end, self.current, self.high, self.low)

  def __repr__(self):
    return self.__str__()