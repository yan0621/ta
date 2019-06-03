
class TradeStrategy(object):
  
  def __init__(self, market):
    self._market = market
    
  def should_open_on_open(self, target, date):
    pass
    
  def should_update_on_open(self, pos, date):
    pass
    
  def analyze(self):
    pass