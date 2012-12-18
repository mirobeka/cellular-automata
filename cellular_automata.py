'''
         _,.--.,_
       .'_..--.._'.
      /.' . 60 . '.\
     // .      / . \\
    |; .      /   . |;
    ||45    ()    15||
    |; .          . |;
     \\ .        . //
      \'._' 30 '_.'/
       '-._'--'_.-'
           `""`
'''
class TimeStep:
  def __init__(self, maxSteps):
    self.time = 0
    self.maxSteps = maxSteps

  def getTime(self):
    return self.time

  def underMaxSteps(self):
    return self.time < self.maxSteps

  def nextStep(self):
    self.time += 1
  
  def previousStep(self):
    self.time -= 1

'''
       , __  T
      /|/  \ 
       |___/ 
       | \   
       |  \_/
             O
'''
class Rule:
  ''' Abstract Rule class '''
  def __init__(self):
    # usually store rules data in self.rules
    self.rules = None

  def getNextState(self, cellStates, neighborsStates):
    raise Exception("method getNextState not implemented")

''' Set of rules for Game of Life version of Cellular Automata '''
class GoLRule(Rule):
  def getNextState(self, cellState, neighborsStates):
    noOfNeighborsAlive = sum(neighborsStates)
    if cellState == 1 and  2 <= noOfNeighborsAlive <= 3:
      return 1
    elif cellState == 0 and noOfNeighborsAlive == 3:
      return 1
    else:
      return 0

class NumberRule(Rule):
  def __init__(self, ruleNumber, numberOfStates, threshold):
    self.rules = {}
    self.numberOfStates = numberOfStates
    self.ruleNumber = ruleNumber
    self.threshold = threshold
    self.rules = self.ruleDisassembler(ruleNumber, numberOfStates, threshold, {})

  def __str__(self):
    return ''.join([str(key) + " => " + str(value) + "\n" for key, value in self.rules.items()])

  def ruleDisassembler(self, number, base, threshold, rules):
    if number is 0:
      return rules
    rules[self.threshold - threshold] = number % base
    return self.ruleDisassembler(number / base, base, threshold-1, rules)

  def getNextState(self, sumOfCellStates):
    if sumOfCellStates >= self.threshold:
      return self.rules[self.threshold]
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

'''
        _|_|_|_|_|_
        _|_|_|_|_|_
        _|_|_|_|_|_
        _|_|_|_|_|_
         | | | | |
'''
class Lattice:
  def __init__(self, width, height, ruleRef):
    self.width = width
    self.height = height

    # lattice initialization
    self.lattice = [[Cell(cellX, cellY, ruleRef) for cellX in range(self.width)] for cellY in range(self.height)]

    # create connections between cells
    self.initializeNeighbors()

  def initializeStateOfCell(self, state, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.lattice[y][x].initializeState(state)

  # set state of particular cell
  def setStateOfCell(self, state, x, y, timeStep):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.lattice[y][x].setState(state, timeStep)

  # get state of particular cell
  def getStateOfCell(self, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      return self.lattice[y][x].getState()

  def getCells(self, listOfIndices):
    listOfCells = []
    for x,y in listOfIndices:
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
        listOfCells.append(None)
      else:
        listOfCells.append(self.lattice[y][x])
    return listOfCells

  def initializeNeighbors(self):
    # add neighbors to each cells list of neighbors
    # map(lambda row: map(lambda cell: cell.addNeighbors(self.getCells(self.vonNeumannNeighborhood(cell.getCoordinates()))), row), self.lattice)
    map(lambda row: map(lambda cell: cell.addNeighbors(self.getCells(self.edieMooreNeighborhood(cell.getCoordinates()))), row), self.lattice)

  def nextTimeStep(self, timeStep):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.nextStep(timeStep), row),self.lattice)

  def vonNeumannNeighborhood(self, (x, y)):
    # returns list of tuples of indices for von Neumann neighborhood
    return [(x+1,y), (x,y+1), (x-1,y), (x, y-1)]

  def edieMooreNeighborhood(self, (x, y)):
    # returns list of tuples of indices for Moore neighborhood
    neighsIndices = [(i,j) for i in range(x-1,x+2) for j in range(y-1,y+2)]
    neighsIndices.remove((x,y))
    return neighsIndices

  def getLattice(self):
    return self.lattice

'''
      _             _
     |_|_ _        |_|_         _   _             _
      _|_|_|      _ _|_|       |_|_|_|        _  |_|
     |_|_|       |_|_|_|         |_|_|       |_|_|_|
                                 |_|           |_|_|
'''
class CellularAutomata:
  def __init__(self, rule):
    self.lattice = Lattice(40,35, rule)

  def getRawData(self):
    return [(cell.x, cell.y, cell.getState(), cell.getSize()) for row in self.lattice.getLattice() for cell in row]

  def setUpInitialConfiguration(self, initialConfiguration):
    map(lambda (state,x,y): self.lattice.initializeStateOfCell(state,x,y), initialConfiguration)

  def nextStep(self, timeStep):
    self.lattice.nextTimeStep(timeStep.getTime())
    timeStep.nextStep()

  def start(self, maxSteps = 10000):
    timeStep = TimeStep(maxSteps)
    while timeStep.underMaxSteps():
      self.nextStep(timeStep)
      print("Step #{0:03d}".format(timeStep.getTime()))
      print(self)

  def checkNeighsSoundness(self):
    self.lattice.checkNeighsSoundness()

  def __str__(self):
    return ''.join([''.join(["{0:02d} ".format(row[0].y)]+[str(cell) for cell in row]) + "|\n" for row in self.lattice.getLattice()])
