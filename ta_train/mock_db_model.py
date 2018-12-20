from datetime import datetime, timedelta
import random
import time

from ta_train.db_model import DB


class MockDB(DB):
  
  def __init__(self):
    self._price_idx = 1

  def execute(self, sql):
    pass
  
  def execute_and_fetch(self, sql):
    if sql == 'select * from Variety':
      return [(1, 'ST', 'SH', 'TEST', '100001')]
    elif sql.startswith('select * from Variety where id = '):
      return [(1, 'ST', 'SH', 'TEST', '100001')]
    elif sql.startswith('select * from Price'):
      mock_prices = []
      if 'start_date >' in sql:
        mock_prices.append((self._price_idx, 1, 'CNY', '1D',
                            pdate,
                            1000 * time.mktime(pdate.timetuple()),
                            oprice,
                            hprice,
                            lprice,
                            cprice,
                            volume,
                            volume * (oprice + cprice) / 2))
        self._price_idx += 1
      else:
        pdate = datetime(2018, 1, 1)
        oprice = 1000
        volume = 100000
        for i in range(1, 100):
          while pdate.weekday() in (0, 6):
            pdate = pdate + timedelta(days=1)
        
          hprice = int(oprice * (1 + 0.1 * random.random()))
          lprice = int(oprice * (1 - 0.1 * random.random()))
          cprice = int(lprice + (hprice - lprice) * random.random())
          volume = int(volume * (0.5 + random.random()))
          mock_prices.append((i, 1, 'CNY', '1D', pdate, 1000 * time.mktime(pdate.timetuple()),
                              oprice,
                              hprice,
                              lprice,
                              cprice,
                              volume,
                              volume * (oprice + cprice) / 2))
          self._price_idx += 1
          oprice = int(cprice * (0.9 + 0.2 * random.random()))
          pdate = pdate + timedelta(days=1)

      return mock_prices
    else:
      return None

  def close(self):
    pass