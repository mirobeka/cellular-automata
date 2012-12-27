class Rule:
  ''' Abstract Rule class '''
  def __init__(self):
    # usually store rules data in self.rules
    self.rules = None

  def getNextState(self, cell, neighbors):
    raise Exception("method getNextState not implemented")

