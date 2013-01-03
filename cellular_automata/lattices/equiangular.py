from __future__ import print_function
from cellular_automata.cells.regular import SquareCell, VariableSquareCell
from cellular_automata.lattices.base import Lattice

class SquareLattice(Lattice):
  def __init__(self, dimensions, neighborhoodMethod, rule):
    self.width, self.height = dimensions
    self.cells = self.initializeLatticeCells(neighborhoodMethod, rule)

  def initializeLatticeCells(self, neighborhoodMethod, rule):
    cells = self.createCells(rule)
    self.initializeNeighbors(cells, neighborhoodMethod)
    return cells

  def createCells(self, rule):
    cells = [[SquareCell(rule) for x in range(self.width)] for y in range(self.height)]
    return cells

  def initializeNeighbors(self, cells, neighborhoodMethod):
    radius = cells[0][0].radius
    for y in range(len(cells)):
      for x in range(len(cells[y])):
        neighs = neighborhoodMethod(cells, x, y)
        cells[y][x].addNeighbors(neighs)
        cells[y][x].setPosition((2*x*radius+radius, 2*y*radius+radius))

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

class VariableSquareLattice(SquareLattice):
  def __init__(self, dimensions, neighborhoodMethod, rule):
    SquareLattice.__init__(self, dimensions, neighborhoodMethod, rule)
    # flatten 2 dimensional list of cells
    self.cells = [cell for row in self.cells for cell in row]

  def createCells(self, rule):
    cells = [[VariableSquareCell(rule) for x in range(self.width)] for y in range(self.height)]
    return cells

  def nextStep(self):
    self.handleGrowingCells()
    map(lambda cell: cell.computeNextState(), self.cells)
    map(lambda cell: cell.applyNextState(), self.cells)

  def handleGrowingCells(self):
    growingCells = [cell for cell in self.cells if cell.wantsGrow()]
    for growingCell in growingCells:
      if growingCell in self.cells:
        changes = growingCell.grow()
        if changes:
          cellsToRemove, cellsToAdd = changes
          self.removeCells(cellsToRemove)
          self.addCells(cellsToAdd)

  def addCells(self, listOfCellsToAdd):
    for cellToAdd in listOfCellsToAdd:
      self.cells.append(cellToAdd)

  def removeCells(self, listOfCellsToRemove):
    for cellToRemove in listOfCellsToRemove:
      self.cells.remove(cellToRemove)

