from st_assistant.data.stock_pos import StockPos


class StockPosLoader(object):

  DEFAULT_POS_FILE = '/Users/yanpan/Documents/stock_pos.txt'

  def __init__(self, pos_file=DEFAULT_POS_FILE):
    self._pos_file = pos_file

  def load(self):
    pass