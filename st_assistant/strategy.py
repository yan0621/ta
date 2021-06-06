from st_assistant.data.stock_pos import StockLevel

class Strategy(object):

  def __init__(self):
    pass

  def getMaxPos(self, stock_pos, current_price):
  	if stock_pos.level == StockLevel.LONG:
  		return 0.2
  	elif stock_pos.level == StockLevel.NML:
  		if stock_pos.rv == 0:
  			return 0.15
  		else:
  			if current_price > 1.05 * stock_pos.rv:
  				return 0.15
  			else:
  				return min(0.025 * (1 + ((1.05 * stock_pos.rv - current_price) / stock_pos.rv) * 100 % 5) + 0.025, 0.15)
  	elif stock_pos.level == StockLevel.TRO:
  		if stock_pos.rv == 0:
  			return 0.05
  		else:
  			if current_price > stock_pos.rv:
  				return 0.05
  			else:
  				return min(0.01 * (1 + ((stock_pos.rv - current_price) / stock_pos.rv) * 100 % 5) + 0.01, 0.05)
  	elif stock_pos.level == StockLevel.UD:
  		if stock_pos.rv == 0:
  			return 0
  		else:
  			if current_price > stock_pos.rv:
  				return 0.05
  			else:
  				return min(0.01 * (1 + ((stock_pos.rv - current_price) / stock_pos.rv) * 100 % 5) + 0.005, 0.05)

  def getRecommendedPos(self, stock_pos, current_price):
  	if stock_pos.level == StockLevel.LONG or stock_pos.level == StockLevel.NML:
  		if stock_pos.rv == 0:
  			return 0
  		else:
  			if current_price > 1.05 * stock_pos.rv:
  				return 0
  			else:
  				return min(0.025 * (1 + ((1.05 * stock_pos.rv - current_price) / stock_pos.rv) * 100 % 5), 0.15)
  	elif stock_pos.level == StockLevel.TRO or stock_pos.level == StockLevel.UD:
  		if stock_pos.rv == 0:
  			return 0
  		else:
  			if current_price > stock_pos.rv:
  				return 0
  			else:
  				return min(0.01 * (1 + ((stock_pos.rv - current_price) / stock_pos.rv) * 100 % 5), 0.05)