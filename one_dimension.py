import operator

class Rule:
  def __init__(self, ruleNumber):
    self.rule = self.createRuleDefinition(ruleNumber)
    # rule could be in following format
    # rule = {
    #   list of states : new state
    #   list of states : new state
    # }

  def createRuleDefinition(self, number):
    return None


  def getNextState(self, configuration):
    return 0
    return self.rule[configuration]


class Cell:
  def __init__(self, x, y, rule, state = 0):
    self.x = x
    self.y = y
    self.neighs = []
    self.state = state
    self.sizeOfCell = 1
    # reference to rule
    self.rule = rule

  def __str__(self):
    nghs = [str(n.getCoordinates()) for n in self.neighs if n]
    return "{}:{} => ".format(self.state,self.getCoordinates()) + str(nghs)

  def nextStep(self):
    self.setState(self.rule([n.state for n in self.neighs]))

  def setState(self, newState):
    self.state = newState

  def addNeighbors(self, listOfNeighbors):
    for neigh in listOfNeighbors:
      self.neighs.append(neigh)

  def getCoordinates(self):
    return (self.x, self.y)

  def getState(self):
    return self.state

  def mergeWithNeighbor(self, neigh):
    # define method to merge 2 cells into 1 bigger cell
    self.sizeOfCell << 1

    # this basically means take all neighbors of neighbor
    # take this cells neighbors and put them together.
    # destroy one of the cell? Which one?
    # increase size of cell
    #
    # I'm not sure about how I'll handle drawing of this cells


class Lattice:
  def __init__(self, width, height, ruleRef):
    self.width = width
    self.height = height

    # lattice initialization
    self.lattice = [[Cell(cellX, cellY, ruleRef) for cellX in range(self.width)] for cellY in range(self.height)]

    # create connections between cells
    self.initializeNeighbors()


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

  def nextTimeStep(self):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.nextStep(), row),self.lattice)

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
  def __init__(self, rule = 90, maxSteps = 1000):
    self.maxSteps = maxSteps
    self.rule = Rule(rule)
    self.lattice = Lattice(100,100, self.rule)

  def start(self):
    timeStep = 0
    while timeStep < self.timeStep:
      self.lattice.nextTimeStep()
      self.drawLattice()

  def drawLattice(self):
    # somehow draw lattice
    pass

  def __str__(self):
    return reduce(operator.concat, [str(cell)+"\n" for row in self.lattice.getLattice() for cell in row])
    

if __name__ == "__main__":
  # create CA and print
  ca = CellularAutomata()
  print(ca)
