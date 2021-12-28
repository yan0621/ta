from st_assistant.data.stock_pos import StockLevel

class Strategy(object):

  def __init__(self):
    pass

  def getWeight(self, stock_pos):
    if stock_pos.level == StockLevel.LUO:
      return 0.1
    elif stock_pos.level == StockLevel.LUR:
      return 0.15
    elif stock_pos.level == StockLevel.LDR:
      return 0.02
    elif stock_pos.level == StockLevel.MUR:
      return 0.05

  def getMaxPos(self, stock_pos):
    return self.getWeight(stock_pos)

  def getRecommendedPos(self, stock_pos, current_price):
    #print(stock_pos)
    if stock_pos.level == StockLevel.LUR:
      if stock_pos.rv == 0:
        return 0
      else:
        if current_price > 1 * stock_pos.rv:
          return 0
        else:
          return min(0.025 * (1 + round(((1 * stock_pos.rv - current_price) / stock_pos.rv) * 20)), 0.15)
    elif stock_pos.level == StockLevel.LUO:
      return 0
    elif stock_pos.level == StockLevel.LDR:
      if stock_pos.rv == 0:
        return 0
      else:
        if current_price > stock_pos.rv:
          return 0
        else:
          return min(0.005 * (1 + round(((stock_pos.rv - current_price) / stock_pos.rv) * 20)), 0.02)
    elif stock_pos.level == StockLevel.MUR:
      return 0