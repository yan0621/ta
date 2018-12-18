from ta_train.db_model import DB


class MockDB(DB):
  
  def __init__(self):
    pass
    
  def execute(self, sql):
    pass
  
  def execute_and_fetch(self, sql):
    if sql == 'select * from Variety':
      return [(1, 'ST', 'SH', 'TEST', '100001')]
    else:
      return None

  def close(self):
    pass