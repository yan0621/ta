import re
import urllib

from st_assistant.data.stock_price import StockPrice


class StockPriceLoader(object):
  
  def __init__(self):
    pass

  def load(self, stock_ids: list):
    pass


class SinaStockPriceLoader(StockPriceLoader):

  SERVICE_URL = 'https://hq.sinajs.cn/list='
  RESP_REG = r'var (.*)="(.*)";'

  def __init__(self):
    pass

  def load(self, stock_ids: list):
    loaded_prices = []
    url = '%s%s' % (self.SERVICE_URL, ','.join(stock_ids))
    with urllib.request.urlopen(url) as f:
      response = f.read().decode('gb2312')
      print(response)
      foundMatches = re.findall(self.RESP_REG, response)
      for match in foundMatches:
        stockId = match[0].split('_')[2]
        prices = match[1].split(',')
        price = StockPrice(
          stock_id=stockId,
          name=prices[0],
          start=float(prices[1]),
          last_end=float(prices[2]),
          current=float(prices[3]),
          high=float(prices[4]),
          low=float(prices[5]))
        loaded_prices.append(price)
    return loaded_prices