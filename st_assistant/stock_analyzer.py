import enum

from st_assistant import strategy

class ActionType(enum.Enum):
  BUY = 1
  SELL = 2


class Action(object):

  def __init__(self, action, target_id, target_name, volume):
    self.action = action
    self.target_id = target_id
    self.target_name = target_name
    self.volume = volume

  def __repr__(self):
    return "%s %s %s %s" % (self.action, self.target_id, self.target_name, self.volume)


class Analyzer(object):

  def __init__(self, stock_pos_list=[], stock_prices=[], cash=0):
    self._pos_list = stock_pos_list
    self._prices = stock_prices
    self._cash = cash

    self._stock_price_dict = dict()
    for price in self._prices:
      self._stock_price_dict[price.id] = price

  def run(self):
    wealth = self.calculateWealth()
    strategy_obj = strategy.Strategy()
    actions = []
    for pos in self._pos_list:
      current_price = self._stock_price_dict[pos.id].current
      pos_rate = pos.pos * current_price / wealth
      max_pos_rate = strategy_obj.getMaxPos(pos, current_price)
      recommended_pos_rate = strategy_obj.getRecommendedPos(pos, current_price)
      print(pos.id, pos.name, pos_rate, max_pos_rate, recommended_pos_rate)
      if pos_rate < recommended_pos_rate:
        action = Action(ActionType.BUY, pos.id, pos.name, (recommended_pos_rate - pos_rate) * wealth)
        actions.append(action)
      elif pos_rate > max_pos_rate:
        action = Action(ActionType.SELL, pos.id, pos.name, (pos_rate - max_pos_rate) * wealth)
        actions.append(action)

    return self.checkAction(actions)


  def calculateWealth(self):
    wealth = 0.0
    for pos in self._pos_list:
      wealth += pos.pos * self._stock_price_dict[pos.id].current
    return wealth + self._cash


  def checkAction(self, action_list):
    checked_actions = []
    sell_actions = []
    long_buy_actions = []
    nml_buy_actions = []
    tro_buy_actions = []
    ud_buy_actions = []
    for action in action_list:
      if action.volume < 100 * self._stock_price_dict[action.target_id].current:
        continue
      else:
        checked_actions.append(action)
    return checked_actions
