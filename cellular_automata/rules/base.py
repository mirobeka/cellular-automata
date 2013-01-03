from random import uniform, randint

class NotImplementedException(Exception):
  pass

class Rule:
  ''' Abstract Rule class '''
  def __init__(self):
    # usually store rules data in self.rules
    self.rules = None

  def getNextState(self, cell, neighbors):
    raise NotImplementedException("method getNextState not implemented")

class DummyRule(Rule):
  def __init__(self, stateVectorLength = 4):
    Rule.__init__(self)
    self.stateVectorLength = stateVectorLength

  def getNextState(self, cell, neighbors):
    state = [randint(0,255) for i in range(self.stateVectorLength-1)]
    growing = 1 if (uniform(0,1) > 0.3) else 0
    state.append(growing)
    return state

  def initialState(self):
    return [0 for i in range(self.stateVectorLength)]
