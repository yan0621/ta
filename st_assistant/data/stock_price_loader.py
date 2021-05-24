import re
import urllib


class StockPriceLoader(object):
  
  def __init__(self):
    pass

  def load(self, stock_ids: list):
  	pass


class SinaStockPriceLoader(StockPriceLoader):

  SERVICE_URL = "https://hq.sinajs.cn/list="
  RESP_REG = r'var (.*)="(.*)";'

  def __init__(self):
  	pass

  def load(self, stock_ids: list):
  	url = '%s%s' % (self.SERVICE_URL, ','.join(stock_ids))
  	with urllib.request.urlopen(url) as f:
  		response = f.read().decode('gb2312')
  		print(response)
  		foundMatches = re.findall(self.RESP_REG, response)
  		for match in foundMatches:
  			stockId = match[0].split('_')[2]
  			prices = match[1].split(',')
  			print(stockId)
  			print(prices)