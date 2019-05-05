
def generate_id():
  if not hasattr(generate_id, 'id_gen'):
    generate_id.id_gen = 0
  generate_id.id_gen += 1
  return generate_id.id_gen


class Order(object):

  def __init__(self, target):
    self.id = generate_id()
    self.target = target
    self.executed = False
    self.execute_msg = None
    
  def __repr__(self):
    return '<id:%s, target:%s>' % (self.id, self.target)


class CloseOrder(Order):
  
  def __init__(self, target, price, quantity):
    super(CloseOrder, self).__init__(target)
    self.price = price
    self.quantity = quantity
    
  def __repr__(self):
    return '<close %s, price:%s, quantity:%s>' % (super(CloseOrder, self).__repr__(), self.price, self.quantity)


class SetSlOrder(Order):
  
  def __init__(self, target, sl):
    super(SetSlOrder, self).__init__(target)
    self.sl = sl
    
  def __repr__(self):
    return '<%s, sl:%s>' % (super(SetSlOrder, self).__repr__(), self.sl)


class CreateOrder(Order):

  def __init__(self, target, action, price):
    super(CreateOrder, self).__init__(target)
    self.action = action
    self.price = price
    
  def __repr__(self):
    return '<%s, action:%s, price:%s>' % (super(CreateOrder, self).__repr__(), self.action, self.price)


class FixedCreateOrder(CreateOrder):
  '''
  action: one of ['long', 'short'].
  target: code of target.
  price: float number, value of price.
  quantity: integer, amount of basic units for trading.
  sl: optional stop loss line.
  '''
  
  def __init__(self, target, action, price, quantity, sl=None):
    super(FixedCreateOrder, self).__init__(target, action, price)
    self.quantity = quantity
    self.sl = sl

  def __repr__(self):
    return '<%s, quantity:%s, sl:%s>' % (super(FixedCreateOrder, self).__repr__(), self.quantity, self.sl)


class FixedRiskCreateOrder(CreateOrder):
  
  def __init__(self, target, action, price, risk_percent, sl=None):
    super(FixedRiskCreateOrder, self).__init__(target, action, price)
    self.risk_percent = risk_percent
    self.sl = sl

  def __repr__(self):
    return '<%s, risk_percent:%s, sl:%s>' % (super(FixedRiskCreateOrder, self).__repr__(), self.risk_percent, self.sl)