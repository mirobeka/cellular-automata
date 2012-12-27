from cellular_automata.cells.regullar import SquareCell
from cellular_automata.lattices.base import Lattice


class SquareLattice(Lattice):
  def __init__(self, width, height, ruleRef):
    self.width = width
    self.height = height

    # lattice initialization
    self.cells = [[SquareCell(cellX, cellY, ruleRef) for cellX in range(self.width)] for cellY in range(self.height)]

    # create connections between cells
    self.initializeNeighbors(self.edieMooreNeighborhood)

  # set state of particular cell
  def setStateOfCell(self, state, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.cells[y][x].setState(state)

  # get state of particular cell
  def getStateOfCell(self, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      return self.cells[y][x].getState()

  def getCells(self, listOfIndices):
    listOfCells = []
    for x,y in listOfIndices:
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
        listOfCells.append(None)
      else:
        listOfCells.append(self.cells[y][x])
    return listOfCells

  def initializeNeighbors(self, neighborhoodMethod):
    # add neighbors to each cells list of neighbors
    map(lambda row: map(lambda cell: cell.addNeighbors(self.getCells(neighborhoodMethod(cell.getCoordinates()))), row), self.cells)

  def nextStep(self):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.computeNextState(), row),self.cells)
    map(lambda row: map(lambda cell: cell.applyNextState(), row),self.cells)

  def vonNeumannNeighborhood(self, (x, y)):
    # returns list of tuples of indices for von Neumann neighborhood
    return [(x+1,y), (x,y+1), (x-1,y), (x, y-1)]

  def edieMooreNeighborhood(self, (x, y)):
    # returns list of tuples of indices for Moore neighborhood
    neighsIndices = [(i,j) for i in range(x-1,x+2) for j in range(y-1,y+2)]
    neighsIndices.remove((x,y))
    return neighsIndices

  def getLattice(self):
    return self.cells

class VariableSquareLattice(Lattice):
  def __init__(self):
    self.cells = []


