'''
       , __  T
      /|/  \ 
       |___/ 
       | \   
       |  \_/
             O
'''
class Rule:
  def __init__(self, ruleNumber, numberOfStates, threshold):
    self.rules = {}
    self.numberOfStates = numberOfStates
    self.ruleNumber = ruleNumber
    self.threshold = threshold
    self.rules = self.ruleDisassembler(ruleNumber, numberOfStates, threshold, {})
    print(self.rules)

  def ruleDisassembler(self, number, base, threshold, rules):
    if number is 0:
      return rules
    rules[threshold] = number % base
    return self.ruleDisassembler(number / base, base, threshold-1, rules)

  def getNextState(self, sumOfCellStates):
    if sumOfCellStates > self.threshold:
      return self.threshold
    return self.rules[sumOfCellStates]

'''
     |--------| 
     |        | 
     |  cell  | 
     |        | 
     |--------|
'''
class Cell:
  def __init__(self, x, y, rule, state = 0):
    self.x = x
    self.y = y
    self.neighs = []
    self.state = [state]
    self.sizeOfCell = 1
    self.rule = rule

  def __str__(self):
    nghs = [str(n.getCoordinates()) for n in self.neighs if n]
    return "{}:{} => ".format(self.getState(),self.getCoordinates()) + str(nghs)

  def nextStep(self, timeStep):
    sumOfNeighsStates = sum([neigh.getState(timeStep) for neigh in self.neighs if neigh])
    sumOfNeighsStates += self.getState(timeStep)
    self.setState(self.rule.getNextState(sumOfNeighsStates),timeStep+1)

  def setState(self, newState, timeStep):
    # assert len(self.state) == timeStep
    self.state += [newState]

  def addNeighbors(self, listOfNeighbors):
    for neigh in listOfNeighbors:
      self.neighs.append(neigh)

  def getCoordinates(self):
    return (self.x, self.y)

  def getState(self, timeStep = -1):
    assert len(self.state) >= timeStep
    return self.state[timeStep]

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


'''
        _|__|__|__|_
        _|__|__|__|_
        _|__|__|__|_
        _|__|__|__|_
         |  |  |  |

'''
class Lattice:
  def __init__(self, width, height, ruleRef):
    self.width = width
    self.height = height

    # lattice initialization
    self.lattice = [[Cell(cellX, cellY, ruleRef) for cellX in range(self.width)] for cellY in range(self.height)]

    # create connections between cells
    self.initializeNeighbors()

  # set state of particular cell
  def setStateOfCell(self, state, x, y):
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      self.lattice[y][x].setState(state)

  # get state of particular cell
  def getStateOfCell(self, x, y):
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      return self.lattice[y][x].getState()

  def initializeNeighbors(self):
    # add neighbors to each cells list of neighbors
    map(lambda row: map(lambda cell: cell.addNeighbors(self.getCells(self.vonNeumannNeighborhood(cell.getCoordinates()))), row), self.lattice)

  def getCells(self, listOfIndices):
    listOfCells = []
    for x,y in listOfIndices:
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
        listOfCells.append(None)
      else:
        listOfCells.append(self.lattice[y][x])
    return listOfCells

  def nextTimeStep(self, timeStep):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.nextStep(timeStep), row),self.lattice)

  def vonNeumannNeighborhood(self, (x, y)):
    # returns list of tuples of indices for von Neumann neighborhood
    return [(x+1,y), (x,y+1), (x-1,y), (x, y-1)]

  def edieMooreNeighborhood(self, x, y):
    # returns list of tuples of indices for Moore neighborhood
    neighsIndices = [(i,j) for i in range(x-1,x+2) for j in range(y-1,y+2)]
    return neighsIndices.remove((x,y))

  def getLattice(self):
    return self.lattice

class CellularAutomata:
  def __init__(self, numberOfStates, rule, threshold, maxSteps = 1000):
    self.maxSteps = maxSteps
    self.rule = Rule(rule, numberOfStates, threshold)
    self.lattice = Lattice(10,10, self.rule)

  def setUpInitialConfiguration(self, initialConfiguration):
    map(lambda (state,x,y): self.lattice.setStateOfCell(state,x,y), initialConfiguration)

  def start(self):
    timeStep = 0
    while timeStep < self.maxSteps:
      self.lattice.nextTimeStep(timeStep)
      timeStep += 1
      print("Step #{}".format(timeStep))
      print(self)

  def drawLattice(self):
    # somehow draw lattice
    pass

  def __str__(self):
    return ''.join([''.join([str(cell.getState())+" " for cell in row]) + "\n" for row in self.lattice.getLattice()])

if __name__ == "__main__":
  # configuration for CA
  numberOfStates = 2
  rule = 37
  threshold = 5
  maxSteps = 10
  # create CA and print
  ca = CellularAutomata(numberOfStates, rule, threshold, maxSteps)
  initialConfiguration = [(1,3,7), (1,2,2)]
  ca.setUpInitialConfiguration(initialConfiguration)
  print(ca)
  ca.start()
