

class Position(object):
  '''
  pos_type: 'long' or 'short'
  '''
  
  def __init__(self, id, target, pos_type, price=0, volume=0, sl=0):
    self.id = id
    self.target = target
    self.pos_type = pos_type
    self.avg_cost = price
    self.volume = volume
    self.sl = sl
    
  def __repr__(self):
    return '<id:%s, target:%s, pos_type:%s, avg_cost:%s, volume:%s, sl:%s>' % (self.id, self.target, self.pos_type, self.avg_cost, self.volume, self.sl)
    
  def increase(self, price, volume):
    self.avg_cost = (self.avg_cost * self.volume + price * volume) / (self.volume + volume)
    self.volume += volume
    
  def decrease(self, volume):
    if (volume >= self.volume):
      self.avg_cost = 0
      self.volume = 0
    else:
      self.volume -= volume