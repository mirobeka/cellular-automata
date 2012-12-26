class Cell:
  def __init__(self, x, y, rule, state = 0):
    self.x = x
    self.y = y
    self.neighs = []
    self.state = [state]
    self.rule = rule
  
  def __str__(self):
    if self.state[-1]:
      return "|*"
    else:
      return "|_"

  def nextStep(self, timeStep):
    neighsStates = [neigh.getState(timeStep) for neigh in self.neighs if neigh]
    newState = self.rule.getNextState(self.getState(timeStep), neighsStates)
    self.setState(newState,timeStep+1)

  def addNeighbors(self, listOfNeighbors):
    for neigh in listOfNeighbors:
      self.neighs.append(neigh)

  def getCoordinates(self):
    return (self.x, self.y)

  def initializeState(self, state):
    self.state[0] = state

  def setState(self, newState, timeStep):
    if timeStep == len(self.state):
      self.state.append(newState)
    else:
      self.state[timeStep] = newState

  def getState(self, timeStep):
    return self.state[timeStep]

  def getNeighbors(self):
    return self.neighs

