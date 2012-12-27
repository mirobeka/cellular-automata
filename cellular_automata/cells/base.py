class Cell:
  def __init__(self, rule):
    self.rule = rule
    self.neighs = None
    self.initState()

  def initState(self):
    self.state = {}
    self.state["current"] = None
    self.state["next"] = None

  def computeNextState(self):
    self.state["next"] = self.rule.getNextState(self, self.neighs)

  def applyNextState(self):
    self.state["current"] = self.state["next"]

  def getState(self):
    return self.state["current"]

  def setState(self, state):
    self.state["current"] = state
  
  def getNeighbors(self):
    raise Exception("method getNeighbors of Cell is not implemented")
