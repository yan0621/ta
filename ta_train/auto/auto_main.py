from datetime import datetime, timedelta

from . import agent
from . import market
from . import trader
from ta_train import logger

import pdb


def get_time_delta(tick_type, count):
  if tick_type == 'day':
    return timedelta(days=count)
  else:
    return None


'''
target_list: [string]
start_date: string, 'yyyy-mm-dd'
end_date: same as start_date
tick_type: string, one of ['day']
'''
def run(target_list, start_date, end_date, tick_type):
  start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
  end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
  logger.info('from %s to %s', start_date_obj, end_date_obj)

  _market = market.Market(target_list)
  _agent = agent.Agent(target_list, _market)
  _trader = trader.Trader('ma', _agent, _market)

  orders = []
  tick_date = start_date_obj
  while tick_date < end_date_obj:
    orders = _trader.get_orders_on_open(target_list, tick_date)
    _agent.execute_orders(orders, tick_date)
    if orders:
      logger.info(str(tick_date))
      logger.info('orders:%s' % str(orders))
      logger.info('pos:%s' % str(_agent.get_pos()))
    _agent.monitor_market(tick_date)
    tick_date = tick_date + get_time_delta(tick_type, 1)

  _agent.analyze()