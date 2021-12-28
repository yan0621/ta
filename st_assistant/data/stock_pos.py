import enum

class StockLevel(enum.Enum):
  LUO = 1
  LUR = 2
  LDR = 3
  MUR = 4

class StockPos(object):

  def __init__(self, stock_id=None, name=None, level=None, rv=None, offset=None, pos=None, pos_value=None):
    self.id = stock_id
    self.name = name
    self.level = level
    self.rv = rv
    self.offset = offset
    self.pos = pos
    self.pos_value = pos_value

  def __str__(self):
    return "{%s, %s, level=%s, rv=%d, pos=%d, pos_v=%d}" % (self.id, self.name, self.level, self.rv if self.rv else 0, self.pos, self.pos_value)

  def __repr__(self):
    return self.__str__()