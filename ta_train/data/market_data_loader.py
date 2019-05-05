from datetime import datetime

from ta_train import logger


class MarketDataLoader(object):
  
  def __init__(self):
    pass
    
    
class FileMarketDataLoader(MarketDataLoader):
  
  def __init__(self):
    pass
    
  def load_from_file(self, file_path):
    line_data_list = []
    with open(file_path) as f:
      for line in f.readlines():
        line_data = self._parse_data_line(line)
        if line_data:
          line_data_list.append(line_data)
    
    return line_data_list
    
  def _parse_data_line(self, line):
    pass
    

class TDXFileMarketDataLoader(FileMarketDataLoader):
  
  def __init__(self):
    pass

  def _parse_data_line(self, line):
    tokens = line.strip().split('\t')
    tokens = [t.replace(' ', '') for t in tokens]
    tokens = [t for t in tokens if t]
    if len(tokens) < 12:
      logger.warn('skip line %s', line)
    else:
      try:
        return {
          'date': tokens[0].replace('/', '-'),
          'open': float(tokens[1]),
          'high': float(tokens[2]),
          'low': float(tokens[3]),
          'close': float(tokens[4]),
          'volume': float(tokens[5]),
          'ma5': float(tokens[6]),
          'ma20': float(tokens[7]),
          'ma60': float(tokens[8]),
        }
      except Exception as e:
        logger.warn(str(e))
        logger.warn('skip line %s', line)
        return None