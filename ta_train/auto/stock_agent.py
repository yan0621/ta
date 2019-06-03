from . import agent

from ta_train.simulated import controller


class StockAgent(agent.Agent):
  
  def __init__(self, target_list, market):
    super(StockAgent, self).__init__(target_list, market)
    
  def _init_controllers(self, target_list):
    self._controller_dict = {}
    for target in target_list:
      self._controller_dict[target] = controller.STController({
          'deposit_rate': 1,
          'fee_config': {
            'method': 'fixed',
            'value': 0.99,
          },
          'hand_size': 1,
      })