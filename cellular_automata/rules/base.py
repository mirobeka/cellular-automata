from random import uniform, randint

class Rule:
  ''' Abstract Rule class '''

  def get_next_state(self, cell, neighbors):
    raise NotImplementedError("method getNextState not implemented")

class DummyRule(Rule):
  def get_next_state(self, cell, neighbors):
    return cell.state.create_random_state()
