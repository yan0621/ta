from ta_train.objects import order
from ta_train import logger

from . import trade_strategy


class BalanceTradeStrategy(trade_strategy.TradeStrategy):
  
  BALANCE_CONFIG = {
    #'vixy': 0.2,
    'tlt': 0.5,
    'spy': 0.5
  }
  MAX_OFFSET = 0.05
  
  def __init__(self, agent, market):
    self._agent = agent
    self._market = market
  
  def should_open_on_open(self, target, date):
    wealth = self._agent.get_wealth() / 2
    prices = self._market.get_recent_price(target, date, 1)
    pos = self._agent.get_target_pos(target)
  
    if not pos:
      return order.FixedCreateOrder(target, 'long', prices[0].open,
                                    round(wealth * self.BALANCE_CONFIG[target] / prices[0].open))

    if wealth * self.BALANCE_CONFIG[target] - pos.volume * prices[0].open >= self.MAX_OFFSET * wealth:
      return order.FixedCreateOrder(target, 'long', prices[0].open,
                                    round((wealth * self.BALANCE_CONFIG[target] - pos.volume * prices[0].open)/ prices[0].open))
    else:
      return None

  def should_update_on_open(self, pos, date):
    wealth = self._agent.get_wealth() / 2
    prices = self._market.get_recent_price(pos.target, date, 1)
    
    if pos.volume * prices[0].open - wealth * self.BALANCE_CONFIG[pos.target] >= self.MAX_OFFSET * wealth:
      return order.CloseOrder(pos.target, prices[0].open,
                              round((pos.volume * prices[0].open - wealth * self.BALANCE_CONFIG[pos.target]) / prices[0].open))
    else:
      return None
      
  def analyze(self):
    pass
