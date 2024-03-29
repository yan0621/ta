import enum
import math

from st_assistant import strategy

class ActionType(enum.Enum):
  BUY = 1
  SELL = 2


class Action(object):

  def __init__(self, action, target_id, target_name, volume, volume_number):
    self.action = action
    self.target_id = target_id
    self.target_name = target_name
    self.volume = volume
    self.volume_number = volume_number

  def __repr__(self):
    return "%s %s %s %s %s" % (self.action, self.target_id, self.target_name, self.volume, self.volume_number)


class Offset(object):

  def __init__(self, id, name, value):
    self.id = id
    self.name = name
    self.value = value

  def __str__(self):
    return "{name=%s, offset=%f}" % (self.name, self.value)

  def __repr__(self):
    return self.__str__()


class Analyzer(object):

  def __init__(self, stock_pos_list=[], stock_prices=[], cash=0):
    self._pos_list = stock_pos_list
    self._prices = stock_prices
    self._cash = cash
    print(self._cash)

    self._stock_price_dict = dict()
    for price in self._prices:
      self._stock_price_dict[price.id] = price

  def run(self):
    wealth = self.calculateWealth()
    print('wealth=', wealth)
    strategy_obj = strategy.Strategy()
    actions = []
    for pos in self._pos_list:
      current_price = self._stock_price_dict[pos.id].current
      if current_price == 0:
        continue # skip offline stock
      pos_rate = pos.pos * current_price / wealth
      pos_v_rate = pos.pos_value / wealth
      max_pos_rate = strategy_obj.getMaxPos(pos)
      recommended_pos_rate = strategy_obj.getRecommendedPos(pos, current_price)
      print('%s %s pos_rate=%f, pos_v_rate=%f, max_pos_rate=%f, recommended_pos_rate=%f' % (pos.id, pos.name, pos_rate, pos_v_rate, max_pos_rate, recommended_pos_rate))
      if pos_v_rate < recommended_pos_rate:
        volume = min(recommended_pos_rate - pos_rate, max_pos_rate - pos_v_rate) * wealth
        action = Action(ActionType.BUY, pos.id, pos.name, volume, math.floor(volume / current_price))
        actions.append(action)
      elif pos_rate > max_pos_rate:
        volume = (pos_rate - max_pos_rate) * wealth
        action = Action(ActionType.SELL, pos.id, pos.name, volume, math.floor(volume / current_price))
        actions.append(action)

    return self.checkAction(actions)

  def runOffset(self):
    strategy_obj = strategy.Strategy()
    wealth = self.calculateWealth()
    offset_list = []
    for pos in self._pos_list:
      current_price = self._stock_price_dict[pos.id].current
      pos_rate = pos.pos * current_price / wealth
      if pos.rv > 0:
        offset = current_price / pos.rv
      else:
        offset = current_price / (pos.pos_value / pos.pos)
      weight = strategy_obj.getWeight(pos)
      offset_list.append(Offset(pos.id, pos.name, pos_rate * offset / weight))

    def takeValue(offset):
      return offset.value

    offset_list.sort(key=takeValue, reverse=True)
    return offset_list

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
      elif action.target_id.startswith('sh688') and action.volume < 200 * self._stock_price_dict[action.target_id].current:
        continue
      else:
        checked_actions.append(action)
    return checked_actions
