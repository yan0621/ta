from ta_train.objects import order

from . import trade_strategy

import pdb


class MATradeStrategy(trade_strategy.TradeStrategy):
  
  FIXED_RISK_PERCENT = 2
  
  def __init__(self, agent, market):
    self._agent = agent
    self._market = market
    
  def should_open_on_open(self, target, date):
    prices = self._market.get_recent_price(target, date, 60)
    ma5 = self._market.get_recent_indicator(target, 'ma5', date, 4)
    ma20 = self._market.get_recent_indicator(target, 'ma20', date, 3)
    ma60 = self._market.get_recent_indicator(target, 'ma60', date, 3)
    if not prices or not ma5 or len(ma5) < 3 or not ma20 or len(ma20) < 2 or not ma60 or len(ma60) < 2:
      return None
    return self._should_open_on_prices(target, prices[0].open, prices[1:], ma5[1:], ma20[1:], ma60[1:])

  def should_update_on_open(self, pos, date):
    prices = self._market.get_recent_price(pos.target, date, 60)
    ma5 = self._market.get_recent_indicator(pos.target, 'ma5', date, 4)
    ma20 = self._market.get_recent_indicator(pos.target, 'ma20', date, 3)
    ma60 = self._market.get_recent_indicator(pos.target, 'ma60', date, 3)
    if not prices or not ma5 or len(ma5) < 3 or not ma20 or len(ma20) < 2 or not ma60 or len(ma60) < 2:
      return None
    return self._should_update_on_prices(pos, prices[0].open, prices[1:], ma5[1:], ma20[1:], ma60[1:])
    
  def _should_open_on_prices(self, target, latest_price_v, history_prices, ma5, ma20, ma60):
    current_pos = self._agent.get_target_pos(target)
    # create or add long orders
    if self._should_create_long(latest_price_v, ma5, ma20, ma60):
      sl = self._look_for_long_sl(history_prices, ma20[0], ma60[0])
      if not current_pos or current_pos.volume == 0:
        return order.FixedRiskCreateOrder(target, 'long', latest_price_v, self.FIXED_RISK_PERCENT, sl)
      elif ma5[0] > ma5[1] and ma5[1] <= ma5[2]:
        if current_pos.avg_cost < sl:
          return order.FixedRiskCreateOrder(target, 'long', latest_price_v, self.FIXED_RISK_PERCENT / 2, sl)

    # create or add short orders
    elif self._should_create_short(latest_price_v, ma5, ma20, ma60):
      sl = self._look_for_short_sl(history_prices, ma20[0], ma60[0])
      if not current_pos or current_pos.volume == 0:
        return order.FixedRiskCreateOrder(target, 'short', latest_price_v, self.FIXED_RISK_PERCENT, sl)
      elif ma5[0] < ma5[1] and ma5[1] >= ma5[2]:
        if current_pos.avg_cost > sl:
          return order.FixedRiskCreateOrder(target, 'short', latest_price_v, self.FIXED_RISK_PERCENT / 2, sl)

    else:
      return None

  def _should_update_on_prices(self, pos, latest_price_v, history_prices, ma5, ma20, ma60):
    if pos.pos_type == 'long':
      if ma5[0] < ma20[0] or ma5[0] < ma20[0] or ma20[0] < ma60[0]:
        # close all
        return order.CloseOrder(pos.target, latest_price_v, pos.volume)
      elif latest_price_v < ma20[0] and history_prices[0].close < ma20[0]:
        # close half
        return order.CloseOrder(pos.target, latest_price_v, pos.volume / 2)
      else:
        sl = self._look_for_long_sl(history_prices, ma20[0], ma60[0])
        if sl > pos.sl:
          return order.SetSlOrder(pos.target, sl)
    elif pos.pos_type == 'short':
      if ma5[0] > ma20[0] or ma5[0] > ma20[0] or ma20[0] > ma60[0]:
        # close all
        return order.CloseOrder(pos.target, latest_price_v, pos.volume)
      elif latest_price_v > ma20[0] and history_prices[0].close > ma20[0]:
        # close half
        return order.CloseOrder(pos.target, latest_price_v, pos.volume / 2)
      else:
        sl = self._look_for_short_sl(history_prices, ma20[0], ma60[0])
        if sl < pos.sl:
          return order.SetSlOrder(pos.target, sl)
  
  def _should_create_long(self, latest_price_v, ma5, ma20, ma60):
    return latest_price_v > ma20[0] and ma5[0] > ma20[0] and ma20[0] > ma60[0] and ma20[0] > ma20[1] and ma60[0] > ma60[1]
  
  def _should_create_short(self, latest_price_v, ma5, ma20, ma60):
    return latest_price_v < ma20[0] and ma5[0] < ma20[0] and ma20[0] < ma60[0] and ma20[0] < ma20[1] and ma60[0] < ma60[1]
    
  def _look_for_long_sl(self, recent_prices, ma20_v, ma60_v):
    #if recent_prices[0].low < recent_prices[1].low:
    #  return max(recent_prices[0].low, ma60_v)
    #else:
    for i in range(1, len(recent_prices)):
      if recent_prices[i].low > ma20_v:
        continue
      if (recent_prices[i].close < recent_prices[i].open or
         (recent_prices[i].low <= recent_prices[i-1].low and recent_prices[i].low <= recent_prices[i+1].low)):
        return max(recent_prices[i].low, ma60_v)
          
    return ma60_v

  def _look_for_short_sl(self, recent_prices, ma20_v, ma60_v):
    #if recent_prices[0].high > recent_prices[1].high:
    #  return min(recent_prices[0].high, ma60_v)
    #else:
    for i in range(1, len(recent_prices)):
      if recent_prices[i].high < ma20_v:
        continue
      if (recent_prices[i].close > recent_prices[i].open or
         (recent_prices[i].high >= recent_prices[i-1].high and recent_prices[i].high >= recent_prices[i+1].high)):
        return min(recent_prices[i].high, ma60_v)

    return ma60_v
    
  def analyze(self):
    pass