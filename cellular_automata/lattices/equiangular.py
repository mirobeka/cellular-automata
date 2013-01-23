from __future__ import print_function
from cellular_automata.cells.regular import SquareCell, VariableSquareCell
from cellular_automata.lattices.base import Lattice

class SquareLattice(Lattice):
  '''
  This lattice is using Square Cells to construct 2 dimensional grid of
  square cells that don't change their topology, size or other properties

  Cells are stored in dictionary where coordinates of cells is key value.
  '''
  def __init__(self):
    self.width = self.height = 0
    self.cells = None

  @classmethod
  def createInitialized(cls, dimensions, neighbourhoodMethod, rule):
    lattice = cls()
    lattice.width, lattice.height = dimensions
    lattice.cells = lattice.initializeLatticeCells(neighbourhoodMethod, rule)
    return lattice

  def initializeLatticeCells(self, neighbourhoodMethod, rule):
    cells = self.createCells(rule)
    self.initializeNeighbours(cells, neighbourhoodMethod)
    return cells

  def createCells(self, rule):
    cells = [[SquareCell(rule) for x in range(self.width)] for y in range(self.height)]
    return cells

  def initializeNeighbours(self, cells, neighbourhoodMethod):
    radius = cells[0][0].radius
    for y in range(len(cells)):
      for x in range(len(cells[y])):
        neighs = neighbourhoodMethod(cells, x, y)
        cells[y][x].addNeighbors(neighs)
        cells[y][x].position = (2*x*radius+radius, 2*y*radius+radius)

  # set state of particular cell
  def setStateOfCell(self, state, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.cells[y][x].setState(state)

  def nextStep(self):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.computeNextState(), row),self.cells)
    map(lambda row: map(lambda cell: cell.applyNextState(), row),self.cells)

  def getLattice(self):
    return self.cells

  @classmethod
  def readFromFile(cls, filename):
    pass

  def saveToFile(self, filename):
    '''
    saves properties of lattice:
      -> width height
      -> for each line cell with state and list of neighbours indices

      what I need for each cell?
    '''
    with open(filename, 'w') as f:
      f.write("{},{}\n".format(self.width, self.height))
      # for cell in cells
      pass

class VariableSquareLattice(SquareLattice):
  '''
  Varialble Square Lattice is lattice which cell can change their size,
  change neighbour connections accordingly to changes in sizes.
  Cells also can be merged together and divided into 4 smaller cells

  Variable Square Lattice is using Variable Square Cells that can change size.
  However this lattice is still regular from angular point of view. That's reason
  why is in module of Equiangular lattices.

  Cells are stored in hash based on their current coordinates on grid.
  '''

  @classmethod
  def createInitialized(cls, dimensions, neighbourhoodMethod, rule):
    lattice = cls()
    lattice.width, lattice.height = dimensions
    lattice.cells = lattice.initializeLatticeCells(neighbourhoodMethod, rule)
    lattice.cells = [cell for row in lattice.cells for cell in row]
    return lattice

  def createCells(self, rule):
    cells = [[VariableSquareCell(rule) for x in range(self.width)] for y in range(self.height)]
    return cells

  def nextStep(self):
    self.handleGrowingCells()
    self.handleDividingCells()
    map(lambda cell: cell.computeNextState(), self.cells)
    map(lambda cell: cell.applyNextState(), self.cells)

  def handleDividingCells(self):
    dividingCells = [cell for cell in self.cells if cell.wantsDivide()]
    for dividingCell in dividingCells:
      changes = dividingCell.divide()
      self.handleChangeInCells(changes)

  def handleGrowingCells(self):
    growingCells = [cell for cell in self.cells if cell.wantsGrow()]
    for growingCell in growingCells:
      if growingCell in self.cells:
        changes = growingCell.grow()
        self.handleChangeInCells(changes)

  def handleChangeInCells(self, changes):
    if changes is not None:
      cellsToRemove, cellsToAdd = changes
      self.removeCells(cellsToRemove)
      self.addCells(cellsToAdd)

  def addCells(self, listOfCellsToAdd):
    for cellToAdd in listOfCellsToAdd:
      self.cells.append(cellToAdd)

  def removeCells(self, listOfCellsToRemove):
    for cellToRemove in listOfCellsToRemove:
      self.cells.remove(cellToRemove)

