import copy
import sys

INIT_WEALTH = 1000000.0


def perror(message):
  sys.stderr.write(message)
  sys.stderr.flush()


class STController(object):
  
  def __init__(self, config):
    self.config = config
    self.profit = 0
    self.unrl_profit = 0
    self.cash = INIT_WEALTH
    self.long_positions = []
    self.short_positions = []
    self.pos_idx = 1
    self.position_dict = {}
    self.default_risk = 2
    
  def get_fee(self, price, hands):
    fee_config = self.config['fee_config']
    if fee_config['method'] == 'by_hand':
      return hands * fee_config['value']
    elif fee_config['method'] == 'by_percent':
      return price * self.config['hand_size'] * hands * fee_config['value']
    elif fee_config['method'] == 'fixed':
      return fee_config['value']
    else:
      raise Exception('Bad fee config!')

  def long(self, price, hands, sl):
    if sl >= price:
      return None

    fee = self.get_fee(price, hands)
    deposit = self.config['deposit_rate'] * price * hands * self.config['hand_size']
    if self.cash < fee + deposit:
      return None
    
    self.update(price)
    position = {
      'id': self.pos_idx,
      'cost': price,
      'hands': hands,
      'deposit': deposit,
      'sl': sl,
      'closed': False,
      'type': 'long',
    }
    self.long_positions.append(position)
    self.position_dict[self.pos_idx] = position
    self.cash -= fee + deposit
    self.profit -= fee
    self.pos_idx += 1
    return position
    
  def long_by_risk(self, risk, price, sl):
    if sl >= price:
      return None

    hands = round(self.get_risk_capacity(risk, price - sl))
    if hands == 0:
      perror('Less than 1 hand can be opened under current risk!')
      return None
  
    return self.long(price, hands, sl)

  def long_by_default_risk(self, price, sl):
    return self.long_by_risk(self.default_risk, price, sl)

  def short(self, price, hands, sl):
    if price >= sl:
      return None
    
    fee = self.get_fee(price, hands)
    deposit = self.config['deposit_rate'] * price * hands * self.config['hand_size']
    if self.cash < fee + deposit:
      return None
    
    self.update(price)
    position = {
      'id': self.pos_idx,
      'cost': price,
      'hands': hands,
      'deposit': deposit,
      'sl': sl,
      'closed': False,
      'type': 'short',
    }
    self.short_positions.append(position)
    self.position_dict[self.pos_idx] = position
    self.cash -= fee + deposit
    self.profit -= fee
    self.pos_idx += 1
    return position
    
  def short_by_risk(self, risk, price, sl):
    if price >= sl:
      return None
    
    hands = round(self.get_risk_capacity(risk, sl - price))
    if hands == 0:
      perror('Less than 1 hand can be opened under current risk!')
      return None
  
    return self.short(price, hands, sl)
    
  def short_by_default_risk(self, price, sl):
    return self.short_by_risk(self.default_risk, price, sl)

  def close_long(self, position, price):
    fee = self.get_fee(price, position['hands'])
    profit = (price - position['cost']) * position['hands'] * self.config['hand_size'] / self.config['deposit_rate']
    print(profit)
    self.cash += position['deposit'] + profit
    self.cash -= fee
    self.profit += profit
    self.profit -= fee
    position['closed'] = True
    
  def close_short(self, position, price):
    fee = self.get_fee(price, position['hands'])
    print(fee)
    profit = (position['cost'] - price) * position['hands'] * self.config['hand_size'] / self.config['deposit_rate']
    print(profit)
    self.cash += position['deposit'] + profit
    self.cash -= fee
    self.profit += profit
    self.profit -= fee
    position['closed'] = True
  
  def close(self, position_id, price, hands=0):
    position = self.position_dict[position_id]
    if not position:
      perror('Position not found!')
      return False
    if hands > position['hands']:
      perror('Hands to close exceeds position hands value!')
      return False
    fee = self.get_fee(price, hands if hands else position['hands'])
    position_to_close = position
    if hands and hands < position['hands']:
      sub_pos = copy.copy(position)
      sub_pos['hands'] = hands
      sub_pos['deposit'] = position['deposit'] * hands / position['hands']
      position['hands'] -= hands
      position_to_close = sub_pos
    
    if position_to_close['type'] == 'long':
      self.close_long(position_to_close, price)
    elif position_to_close['type'] == 'short':
      self.close_short(position_to_close, price)
    else:
      perror('Unsupported position type %s!' % position_to_close['type'])
      return False
    
    self.update(price)
    return True
    
  def update(self, price):
    unrl_profit = 0
    for position in self.long_positions:
      if not position['closed']:
        if position['sl'] >= price:
          self.close_long(position, position['sl'])
        else:
          unrl_profit += (price - position['cost']) * position['hands'] * self.config['hand_size'] / self.config['deposit_rate']
    for position in self.short_positions:
      if not position['closed']:
        if position['sl'] <= price:
          self.close_short(position, position['sl'])
        else:
          unrl_profit += (position['cost'] - price) * position['hands'] * self.config['hand_size'] / self.config['deposit_rate']
    self.unrl_profit = unrl_profit
    return self.get_statistics()
  
  def set_sl(self, sl, id=0):
    for position in self.long_positions:
      if id > 0 and position['id'] == id:
        position['sl'] = sl
        return
      elif not position['closed']:
        position['sl'] = sl
    for position in self.short_positions:
      if id > 0 and position['id'] == id:
        position['sl'] = sl
        return
      elif not position['closed']:
        position['sl'] = sl
  
  def set_default_risk(self, risk):
    self.default_risk = risk
  
  def get_risk_capacity(self, percent, offset):
    '''Ammount of hands with given risk percent and price offset.'''
    return (INIT_WEALTH + self.profit) * percent * self.config['deposit_rate'] / (offset * 100.0 * self.config['hand_size']);
    
  def get_statistics(self):
    open_position_num = 0
    for p in self.long_positions:
      if not p['closed']:
        open_position_num += 1
    for p in self.short_positions:
      if not p['closed']:
        open_position_num += 1
    
    opened_long_positions = [p for p in self.long_positions if p['closed'] != True]
    opened_short_positions = [p for p in self.short_positions if p['closed'] != True]
    
    return {
      'cash': self.cash,
      'positions_long': opened_long_positions,
      'positions_short': opened_short_positions,
      'open_position_number': open_position_num,
      'unrl_profit': self.unrl_profit,
      'unrl_profit_rate': self.unrl_profit / (self.profit + INIT_WEALTH),
      'profit': self.profit + self.unrl_profit,
      'profit_rate': (self.profit + self.unrl_profit) / INIT_WEALTH,
      'wealth': self.profit + self.unrl_profit + INIT_WEALTH,
    }