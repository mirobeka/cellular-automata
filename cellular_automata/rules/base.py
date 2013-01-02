from random import uniform, randint

class Rule:
  ''' Abstract Rule class '''
  def __init__(self):
    # usually store rules data in self.rules
    self.rules = None

  def getNextState(self, cell, neighbors):
    raise Exception("method getNextState not implemented")

class DummyRule(Rule):
  def __init__(self):
    Rule.__init__(self)

  def getNextState(self, cell, neighbors):
    state = [randint(0,255), randint(0,255), randint(0,255)]
    growing = 1 if (uniform(0,1) > 0.3) else 0
    state.append(growing)
    return state

  def initialState(self):
    return [255,255,255,0]
