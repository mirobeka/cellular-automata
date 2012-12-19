class Cell:
  def __init__(self, x, y, rule, state = 0):
    self.x = x
    self.y = y
    self.neighs = []
    self.state = [state]
    self.sizeOfCell = 1
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

  def getSize(self):
    return self.sizeOfCell

  def getNeighbors(self):
    return self.neighs

  def replaceNeigh(self, oldNeigh, newNeigh):
    # replace old neighbor with new one
    self.neighs = [newNeigh if oldNeigh == n else n for n in self.neighs]

  def updateNeighborsConnections(self, newNeighs):
    # update connections
    map(lambda neigh: neigh.replaceNeigh(self), newNeighs)

    # absorb means that this cell will sustain, the other will be terminated
  def absorbNeighbor(self, neigh):
    # add new neighbors
    self.addNeighbors(neigh.getNeighbors())

    # for each new neighbor we have to update connection
    self.updateNeighborsConnections(neigh.getNeighbors())

    # cell grows
    self.sizeOfCell << 1

  def splitCell(self):
    # split cell into 2 separate cells.
    pass
