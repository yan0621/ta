import re
import urllib

from st_assistant.data.stock_price import StockPrice


class StockPriceLoader(object):
  
  def __init__(self):
    pass

  def load(self, stock_ids: list):
    pass


class SinaStockPriceLoader(StockPriceLoader):

  FAKE_PRICE_FILE = '/Users/yanpan/Documents/fake_stock_price_data.txt'
  SERVICE_URL = 'https://hq.sinajs.cn/list='
  RESP_REG = r'var (.*)="(.*)";'
  HK_EX_CNY_RATE = 0.82

  def load(self, stock_ids: list):
    url = '%s%s' % (self.SERVICE_URL, ','.join(stock_ids))
    with urllib.request.urlopen(url) as f:
      response = f.read().decode('gb2312')
      print(response)
      return self.loadFromData(response)

  def loadFromDataFile(self):
    with open(self.FAKE_PRICE_FILE) as f:
      return self.loadFromData(f.read())

  def loadFromData(self, stock_price_data):
    loaded_prices = []
    foundMatches = re.findall(self.RESP_REG, stock_price_data)
    for match in foundMatches:
      stockId = match[0].split('_')[2]
      prices = match[1].split(',')
      if stockId.startswith('sh') or stockId.startswith('sz'):
        price = self.parseSHSZPrice(stockId, prices)
      elif stockId.startswith('hk'):
        price = self.parseHKPrice(stockId, prices)
      loaded_prices.append(price)
    return loaded_prices

  def parseSHSZPrice(self, stockId, prices):
    return StockPrice(
      stock_id=stockId,
      name=prices[0],
      start=float(prices[1]),
      last_end=float(prices[2]),
      current=float(prices[3]),
      high=float(prices[4]),
      low=float(prices[5]))

  def parseHKPrice(self, stockId, prices):
    return StockPrice(
      stock_id=stockId,
      name=prices[1],
      start=float(prices[2]) * self.HK_EX_CNY_RATE,
      last_end=float(prices[3]) * self.HK_EX_CNY_RATE,
      current=float(prices[4]) * self.HK_EX_CNY_RATE,
      high=float(prices[5]) * self.HK_EX_CNY_RATE,
      low=float(prices[6]) * self.HK_EX_CNY_RATE)