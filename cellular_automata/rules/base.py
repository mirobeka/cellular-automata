from random import uniform

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
    return [1 if (uniform(0,1) > 0.5) else 0 for x in range(2)]
