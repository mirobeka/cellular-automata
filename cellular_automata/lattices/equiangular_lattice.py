from cellular_automata.cells.cell import Cell
from cellular_automata.lattices.lattice import Lattice

class EquiangularLattice(Lattice):
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
