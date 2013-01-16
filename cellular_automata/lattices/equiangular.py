from __future__ import print_function
from cellular_automata.cells.regular import SquareCell, VariableSquareCell
from cellular_automata.lattices.base import Lattice
import pyopencl as cl
import numpy

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

class FastSquareLattice(SquareLattice):
  def __init__(self, dimensions, neighbourhoodMethod, rule):
    SquareLattice.__init__(self,dimensions, neighbourhoodMethod, rule)
    self.rule = rule
    self.flatCells = [cell for row in self.cells for cell in row]
    self.initOpenCL()

  def initOpenCL(self):
    self.ctx = cl.create_some_context()
    self.queue = cl.CommandQueue(self.ctx)
    self.program = cl.Program(self.ctx, self.rule.getKernel()).build()

  def nextStep(self):
    # prepare arrays
    stateVector = numpy.array(map(lambda cell: cell.getState(), self.flatCells))
    aliveVector = numpy.array(map(lambda cell: cell.livingNeighbours(), self.flatCells))

    mf = cl.mem_flags
    stateVector_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=stateVector)
    aliveVector_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=aliveVector)
    newStateVector_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, aliveVector.nbytes)

    self.program.golrule(self.queue, stateVector.shape, None, stateVector_buf, aliveVector_buf, newStateVector_buf)

    newStateVector = numpy.empty_like(stateVector)
    cl.enqueue_read_buffer(self.queue, newStateVector_buf, newStateVector).wait()
    print(newStateVector)

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

