INIT_WEALTH = 1000000.0

class STController(object):
  
  def __init__(self, config):
    self.config = config
    self.profit = 0
    self.unrl_profit = 0
    self.cash = INIT_WEALTH
    self.long_positions = []
    self.short_positions = []
    self.pos_idx = 1
    
  def get_fee(self, price, hands):
    fee_config = self.config['fee_config']
    if fee_config['method'] == 'by_hand':
      return hands * fee_config['value']
    elif fee_config['method'] == 'by_percent':
      return price * self.config['hand_size'] * hands * fee_config['value']
    else:
      raise Exception('Bad fee config!')

  def long(self, price, hands, sl):
    if sl >= price:
      return False

    volume = self.config['hand_size'] * hands
    fee = self.get_fee(price, hands)
    deposit = self.config['deposit_rate'] * price * volume
    if self.cash < fee + deposit:
      return False
    
    self.update(price)
    self.long_positions.append({
      'id': self.pos_idx,
      'cost': price,
      'hands': hands,
      'volume': volume,
      'deposit': deposit,
      'sl': sl,
      'closed': False,
    })
    self.cash -= fee + deposit
    self.profit -= fee
    self.pos_idx += 1
    return True

  def short(self, price, hands, sl):
    if price >= sl:
      return False
    
    volume = self.config['hand_size'] * hands
    fee = self.get_fee(price, hands)
    deposit = self.config['deposit_rate'] * price * volume
    if self.cash < fee + deposit:
      return False
    
    self.update(price)
    self.short_positions.append({
      'id': self.pos_idx,
      'cost': price,
      'hands': hands,
      'volume': volume,
      'deposit': deposit,
      'sl': sl,
      'closed': False,
    })
    self.cash -= fee + deposit
    self.profit -= fee
    self.pos_idx += 1
    return True

  def close_long(self, position, price):
    fee = self.get_fee(price, position['hands'])
    profit = (price - position['cost']) * position['volume'] / self.config['deposit_rate']
    self.cash += position['deposit'] + profit
    self.cash -= fee
    self.profit += profit
    self.profit -= fee
    position['closed'] = True
    
  def close_short(self, position, price):
    fee = self.get_fee(price, position['hands'])
    profit = (position['cost'] - price) * position['volume'] / self.config['deposit_rate']
    self.cash += position['deposit'] + profit
    self.cash -= fee
    self.profit += profit
    self.profit -= fee
    position['closed'] = True

  def update(self, price):
    unrl_profit = 0
    for position in self.long_positions:
      if not position['closed']:
        if position['sl'] >= price:
          self.close_long(position, price)
        else:
          unrl_profit += (price - position['cost']) * position['volume'] / self.config['deposit_rate']
    for position in self.short_positions:
      if not position['closed']:
        if position['sl'] <= price:
          self.close_short(position, price)
        else:
          unrl_profit += (position['cost'] - price) * position['volume'] / self.config['deposit_rate']
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
  
  def get_risk_capacity(self, percent, offset):
    '''Ammount of hands with given risk percent and price offset.'''
    return (INIT_WEALTH + self.profit) * percent * self.config['deposit_rate'] / (offset * 100.0 * self.config['hand_size']);
    
  def get_statistics(self):
    return {
      'cash': self.cash,
      'positions_long': self.long_positions,
      'positions_short': self.short_positions,
      'profit': self.profit + self.unrl_profit,
      'profit_rate': (self.profit + self.unrl_profit) / INIT_WEALTH,
    }