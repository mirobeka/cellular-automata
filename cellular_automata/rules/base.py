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
  def __init__(self, stateVectorLength = 5):
    Rule.__init__(self)
    self.stateVectorLength = stateVectorLength

  def getNextState(self, cell, neighbors):
    state = [randint(0,255) for i in range(self.stateVectorLength-2)]
    growing = 1 if (uniform(0,1) > 0.5) else 0
    dividing = 1 - growing
    state.append(growing)
    state.append(dividing)
    return state

  def initialState(self):
    return [0 for i in range(self.stateVectorLength)]

class AllwaysMergeRule(DummyRule):
  def getNextState(self, cell, neighbors):
    state = [randint(0,255) for i in range(self.stateVectorLength-2)]
    state.append(1) # growing
    state.append(0) # dividing
    return state

  def initialState(self):
    state = [1 for i in range(self.stateVectorLength-1)]
    state.append(0)
    return state

