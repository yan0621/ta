import datetime
import os

from ta_train.data import market_data_loader
from ta_train.objects import price
from ta_train import logger

import pdb


class Market(object):
  
  DATA_DIR_PATH = '/Users/yanpan/Documents/mdata'
  
  def __init__(self, target_list):
    self._loader = market_data_loader.TDXFileMarketDataLoader()
    self._data = {}
    self._load_data(target_list)
    
  def _load_data(self, target_list):
    for target in target_list:
      logger.info('load data for %s', target)
      file_path = '%s/%sL9.txt' % (self.DATA_DIR_PATH, target.upper())
      if os.path.exists(file_path):
        self._load_file_data(target, file_path)
      else:
        file_path = '%s/%s.txt' % (self.DATA_DIR_PATH, target.upper())
        self._load_file_data(target, file_path)

  def _load_file_data(self, target, file):
    data_list = self._loader.load_from_file(file)
    prices = []
    price_idx_dict = {}
    ma5 = []
    ma5_idx_dict = {}
    ma20 = []
    ma20_idx_dict = {}
    ma60 = []
    ma60_idx_dict = {}
    for data in data_list:
      prices.append(price.Price(data['open'], data['high'], data['low'], data['close'], data['volume']))
      price_idx_dict[data['date']] = len(prices) - 1
      ma5.append(data['ma5'])
      ma5_idx_dict[data['date']] = len(ma5) - 1
      ma20.append(data['ma20'])
      ma20_idx_dict[data['date']] = len(ma20) - 1
      ma60.append(data['ma60'])
      ma60_idx_dict[data['date']] = len(ma60) - 1
    self._data[target] = {
      'prices': prices,
      'price_idx_dict': price_idx_dict,
      'ma5': ma5,
      'ma5_idx_dict': ma5_idx_dict,
      'ma20': ma20,
      'ma20_idx_dict': ma20_idx_dict,
      'ma60': ma60,
      'ma60_idx_dict': ma60_idx_dict,
    }

  def _get_date_key_str(self, date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')
    
  def get_price(self, target, date):
    idx = self._data[target]['price_idx_dict'].get(self._get_date_key_str(date), None)
    if not idx:
      return None
    return self._data[target]['prices'][idx]
    
  def get_recent_price(self, target, date, days_before=0):
    idx = self._data[target]['price_idx_dict'].get(self._get_date_key_str(date), None)
    if not idx or idx < days_before:
      return None
    result = self._data[target]['prices'][idx - days_before : idx + 1]
    result.reverse()
    return result

  def get_recent_indicator(self, target, name, date, days_before=0):
    vlist = None
    date_dict = None
    if name == 'ma5':
      vlist = self._data[target]['ma5']
      date_dict = self._data[target]['ma5_idx_dict']
    elif name == 'ma20':
      vlist = self._data[target]['ma20']
      date_dict = self._data[target]['ma20_idx_dict']
    elif name == 'ma60':
      vlist = self._data[target]['ma60']
      date_dict = self._data[target]['ma60_idx_dict']
    
    idx = date_dict.get(self._get_date_key_str(date), None)
    if not idx or idx < days_before:
      return None
    result = vlist[idx - days_before : idx + 1]
    result.reverse()
    return result

  def is_open(self, target, date):
    return self._get_date_key_str(date) in self._data[target]['price_idx_dict']