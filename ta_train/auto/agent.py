from ta_train.config import ta_config
from ta_train.objects.position import Position
from ta_train.objects.order import CloseOrder, SetSlOrder, FixedCreateOrder, FixedRiskCreateOrder
from ta_train.simulated import controller
from ta_train import logger

import pdb


class Agent(object):
  '''
  _target_pos: target(str) -> pos(Position.obj)
  _pos_id_dict: position id(integer) -> controller position id(integer)
  '''
  
  def __init__(self, target_list, market):
    self._market = market
    self._init_controllers(target_list)
    self._target_pos = {}
    self._pos_id_dict = {}
    
  def _init_controllers(self, target_list):
    self._controller_dict = {}
    for target in target_list:
      self._controller_dict[target] = controller.STController(ta_config.TA_CONFIG['FT'][target])

  def _get_controller(self, target):
    return self._controller_dict[target]
    
  def execute_orders(self, orders, date):
    failed_orders = []
    for order in orders:
      #if date.month == 2 and date.day >= 4:
      #  pdb.set_trace()
      if not self._validate_order(order):
        continue
      
      controller = self._get_controller(order.target)
      if isinstance(order, CloseOrder):
        cpos_id = self._pos_id_dict[self._target_pos[order.target].id]
        controller.close(cpos_id, price=order.price, hands=order.quantity)
        self._target_pos[order.target].decrease(order.quantity)
        logger.info('close pos %s' % self._target_pos[order.target].id)
      elif isinstance(order, SetSlOrder):
        controller.set_sl(order.sl)
        self._target_pos[order.target].sl = order.sl
      else:
        cpos = self._controller_execute_create_order(controller, order)
        if not cpos:
          order.executed_msg = 'failed'
          failed_orders.append(order)
        else:
          order.executed = True
          if order.target in self._target_pos and self._target_pos[order.target].volume > 0:
            self._target_pos[order.target].increase(order.price, cpos['hands'])
          else:
            self._target_pos[order.target] = Position(order.id, order.target, order.action, cpos['cost'], cpos['hands'], order.sl)
            self._pos_id_dict[self._target_pos[order.target].id] = cpos['id']

  def _validate_order(self, order):
    if isinstance(order, CloseOrder):
      if order.target not in self._target_pos:
        logger.warn('Trying to close a pos that does not exist!')
        return False
      else:
        return True
    else:
      return True
  
  def _controller_execute_create_order(self, controller, order):
    if order.action == 'long':
      if isinstance(order, FixedCreateOrder):
        return controller.long(order.price, order.quantity, order.sl)
      elif isinstance(order, FixedRiskCreateOrder):
        return controller.long_by_risk(order.risk_percent, order.price, order.sl)
      else:
        logger.warn('unknown order type found!')
        return None
    elif order.action == 'short':
      if isinstance(order, FixedCreateOrder):
        return controller.short(order.price, order.quantity, order.sl)
      elif isinstance(order, FixedRiskCreateOrder):
        return controller.short_by_risk(order.risk_percent, order.price, order.sl)
      else:
        logger.warn('unknown order type found!')
        return None
    else:
      logger.warn('unknown order action %s found!' % order.action)
      return None


  def monitor_market(self, date):
    updated = False
    for target, pos in self._target_pos.items():
      if pos.volume <=0 or not self._market.is_open(target, date) or not pos.sl:
        continue
      price = self._market.get_price(target, date)
      cpos_id = self._pos_id_dict[pos.id]
      controller = self._get_controller(target)
      if pos.pos_type == 'long' and price.low < pos.sl:
        logger.info('auto close long order: low = %s, sl = %s', price.low, pos.sl)
        controller.update(price.low)
        pos.decrease(pos.volume)
        logger.info('close pos %s' % pos.id)
        updated = True
      elif pos.pos_type == 'short' and price.high > pos.sl:
        logger.info('auto close short order: high = %s, sl = %s', price.high, pos.sl)
        controller.update(price.high)
        pos.decrease(pos.volume)
        logger.info('close pos %s' % pos.id)
        updated = True
      controller.update(price.close)
    return updated

  def analyze(self):
    for target, controller in self._controller_dict.items():
      stat = controller.get_statistics()
      logger.info(str(stat))
      logger.info('%s: %s' % (target, stat['profit_rate'] + stat['unrl_profit_rate']))

  def get_pos(self):
    return [p for (t, p) in self._target_pos.items() if p.volume > 0]

  def get_target_pos(self, target):
    return self._target_pos.get(target, None)
    
  def get_wealth(self):
    wealth = 0
    for target, controller in self._controller_dict.items():
      stat = controller.get_statistics()
      wealth += stat['wealth']
    
    return wealth
    
  def get_target_stat(self, target):
    return self._controller_dict[target].get_statistics()