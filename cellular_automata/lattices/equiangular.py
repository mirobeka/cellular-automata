from __future__ import print_function
from cellular_automata.cells.regular import SquareCell, VariableSquareCell
from cellular_automata.lattices.base import Lattice
import yaml

class SquareLattice(Lattice):
  '''
  This lattice is using Square Cells to construct 2 dimensional grid of
  square cells that don't change their topology, size or other properties

  Cells are stored in dictionary where coordinates of cells is key value.
  '''
  def __init__(self):
    Lattice.__init__(self)
    self.cells = None
    self.resolution = 0

  @classmethod
  def createInitialized(cls, **kwargs):
    lattice = cls()
    lattice.width, lattice.height = kwargs["dimensions"]
    lattice.resolution = kwargs["resolution"]                  # use configuration class to pass all of this arguments. Or just use **kwarg
    lattice.cells = lattice.initializeLatticeCells(kwargs["neighbourhoodMethod"], kwargs["rule"])
    return lattice

  def initializeLatticeCells(self, neighbourhoodMethod, rule):
    cells = self.createCells(rule)
    self.initializeNeighbours(cells, neighbourhoodMethod)
    return cells

  def createCells(self, rule):
    cells = {}
    for x in range(0, self.width, self.resolution):
      for y in range(0, self.height, self.resolution):
        cells[(x,y)] = SquareCell.createInitialized(rule)
        coordinates = (x+self.resolution/2, y+self.resolution/2)
        cells[(x,y)].position = coordinates
        cells[(x,y)].radius = self.resolution/2
    return cells

  def initializeNeighbours(self, cells, neighbourhoodMethod):
    for (x,y), cell in cells.items():
      neighs = neighbourhoodMethod(cells, self.resolution, x, y)
      cells[(x,y)].addNeighbors(neighs)

  # set state of particular cell
  def setStateOfCell(self, state, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.cells[(x,y)].state = state

  def nextStep(self):
    # iterate over all cells and go to next state
    map(lambda cell: cell.computeNextState(), self.cells.values())
    map(lambda cell: cell.applyNextState(), self.cells.values())
    self.time += 1

  def run(self, stop_criterion):
    while stop_criterion.should_run(self):
      self.nextStep()

  def getLattice(self):
    return self.cells.values()

  @classmethod
  def fromYAML(cls, configuration):
    '''Read all properties and create lattice with defined
    dimensions and resolution. populate lattice with defined cells.'''
    lattice = cls()
    lattice.width, lattice.height = configuration["dimensions"]
    lattice.resolution = configuration["resolution"]
    lattice.cells = {}

    # fill up lattice with cells
    for cellConfiguration in configuration["cells"]:
      cell = SquareCell.createEmpty()
      print("{}".format(cellConfiguration))
      cell.position = cellConfiguration["position"]
      cell.state = cellConfiguration["state"]
      for direction, neighbours in cellConfiguration["neighbours"]:
        cell.neighs[direction] = neighbours
      lattice.cells[cell.position] = cell

    # change positions of cell neighbours for pointers to those cells
    for cell in lattice.cells.values():
      for direction, directionNeighs in cell.neighs.items():
        cell.neighs[direction] = [lattice.cells[neigh] for neigh in directionNeighs]

    return lattice

  def toYAML(self):
    ''' export all lattice properties and cells into yaml '''
    lattice = {}
    lattice["dimensions"] = (self.width, self.height)
    lattice["resolution"] = self.resolution
    cells = []
    for cell in self.cells.values():
      cells.append(cell.toDict())
    lattice["cells"] = cells
    return yaml.dump(lattice)

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

  def createCells(self, rule):
    cells = {}
    for x in range(0, self.width, self.resolution):
      for y in range(0, self.height, self.resolution):
        coordinates = (x+self.resolution/2, y+self.resolution/2)
        cells[coordinates] = VariableSquareCell.createInitialized(rule)
        cells[coordinates].position = coordinates
        cells[coordinates].radius = self.resolution/2
    return cells

  def nextStep(self):
    self.handleGrowingCells()
    self.handleDividingCells()
    map(lambda cell: cell.computeNextState(), self.cells.values())
    map(lambda cell: cell.applyNextState(), self.cells.values())

  def handleDividingCells(self):
    dividingCells = [cell for cell in self.cells.values() if cell.wantsDivide()]
    for dividingCell in dividingCells:
      changes = dividingCell.divide()
      self.handleChangeInCells(changes)

  def handleGrowingCells(self):
    growingCells = [cell for cell in self.cells.values() if cell.wantsGrow()]
    for growingCell in growingCells:
      if growingCell in self.cells.values(): # additional check if cell wasn't already merged
        changes = growingCell.grow()
        self.handleChangeInCells(changes)

  def handleChangeInCells(self, changes):
    if changes is not None:
      cellsToRemove, cellsToAdd = changes
      self.removeCells(cellsToRemove)
      self.addCells(cellsToAdd)

  def addCells(self, listOfCellsToAdd):
    for cellToAdd in listOfCellsToAdd:
      self.cells[cellToAdd.position] = cellToAdd

  def removeCells(self, listOfCellsToRemove):
    for cellToRemove in listOfCellsToRemove:
      try:
        del self.cells[cellToRemove.position]
      except KeyError as e:
        print("cell at {} not in self.cells".format(cellToRemove.position))

