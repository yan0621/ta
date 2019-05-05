
class TradeStrategy(object):
  
  def __init__(self, market):
    self._market = market
    
  def should_open_on_open(self, target, date):
    pass
    
  def should_close_on_open(self, pos, date):
    pass
    
  def should_open_on_close(self, target, date):
    pass
    
  def should_close_on_close(self, pos, date):
    pass