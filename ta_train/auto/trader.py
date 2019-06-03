from . import ma_trade_strategy
from . import balance_trade_strategy


class Trader(object):
  
  def __init__(self, trade_strategy, agent, market):
    self._agent = agent
    self._market = market
    self._load_strategy(trade_strategy)

  def get_orders_on_open(self, target_list, date):
    orders = []
    # process existing orders
    pos_list = self._agent.get_pos()
    for pos in pos_list:
      if not self._market.is_open(pos.target, date):
        continue
      order = self._strategy.should_update_on_open(pos, date)
      if order:
        orders.append(order)

    # create new orders
    for target in target_list:
      if not self._market.is_open(target, date):
        continue
      order = self._strategy.should_open_on_open(target, date)
      if order:
        orders.append(order)

    return orders
    
  def _load_strategy(self, strategy_name):
    strategy = None
    if strategy_name == 'ma':
      strategy = ma_trade_strategy.MATradeStrategy(self._agent, self._market)
    elif strategy_name == 'balance':
      strategy = balance_trade_strategy.BalanceTradeStrategy(self._agent, self._market)

    self._strategy = strategy
    
  def analyze(self):
    self._strategy.analyze()