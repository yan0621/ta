from st_assistant.data.stock_pos import StockLevel

class Strategy(object):

  def __init__(self):
    pass

  def getWeight(self, stock_pos):
    if stock_pos.level == StockLevel.LONG:
      return 0.2
    elif stock_pos.level == StockLevel.NML:
      return 0.15
    elif stock_pos.level == StockLevel.TRO:
      return 0.05
    elif stock_pos.level == StockLevel.UD:
      return 0.05

  def getMaxPos(self, stock_pos):
    return self.getWeight(stock_pos)

  def getRecommendedPos(self, stock_pos, current_price):
    #print(stock_pos)
    if stock_pos.level == StockLevel.LONG or stock_pos.level == StockLevel.NML:
      if stock_pos.rv == 0:
        return 0
      else:
        if current_price > 1.05 * stock_pos.rv:
          return 0
        else:
          return min(0.025 * (1 + round(((1.05 * stock_pos.rv - current_price) / stock_pos.rv) * 20)), 0.15)
    elif stock_pos.level == StockLevel.TRO or stock_pos.level == StockLevel.UD:
      if stock_pos.rv == 0:
        return 0
      else:
        if current_price > stock_pos.rv:
          return 0
        else:
          return min(0.01 * (1 + round(((stock_pos.rv - current_price) / stock_pos.rv) * 20)), 0.05)