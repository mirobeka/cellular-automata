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
    lattice.resolution = kwargs["resolution"]    # use configuration class to pass all of this arguments. Or just use **kwarg
    lattice.neighbourhood = kwargs["neighbourhood"]
    lattice.rule = kwargs["rule"]
    lattice.cell_state_class = kwargs["state"]
    lattice.cells = lattice.initializeLatticeCells(kwargs["rule"])
    return lattice

  def initializeLatticeCells(self, rule):
    cells = self.createCells(rule)
    self.initializeNeighbours(cells)
    return cells

  def createCells(self, rule):
    cells = {}
    for x in range(0, self.width, self.resolution):
      for y in range(0, self.height, self.resolution):
        cells[(x,y)] = SquareCell.createInitialized(rule, self.neighbourhood, self.cell_state_class)
        coordinates = (x+self.resolution/2, y+self.resolution/2)
        cells[(x,y)].position = coordinates
        cells[(x,y)].radius = self.resolution/2
    return cells

  def initializeNeighbours(self, cells):
    for (x,y), cell in cells.items():
      neighs = self.neighbourhood.gather_neighbours(cells, self.resolution, x, y)
      cells[(x,y)].set_neighbours(neighs)

  # set state of particular cell
  def setStateOfCell(self, state, x, y):
    if x >= 0 or x < self.width or y >= 0 or y < self.height:
      self.cells[(x,y)].state = state

  def nextStep(self):
    # iterate over all cells and go to next state
    map(lambda cell: cell.compute_next_state(), self.cells.values())
    map(lambda cell: cell.apply_next_state(), self.cells.values())
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
        cells[coordinates] = VariableSquareCell.createInitialized(rule, self.neighbourhood)
        cells[coordinates].position = coordinates
        cells[coordinates].radius = self.resolution/2
    return cells

  def nextStep(self):
    self.handleGrowingCells()
    self.handleDividingCells()
    map(lambda cell: cell.compute_next_state(), self.cells.values())
    map(lambda cell: cell.apply_next_state(), self.cells.values())

  def handleDividingCells(self):
    dividing_cells = [cell for cell in self.cells.values() if cell.wantsDivide()]
    for dividing_cell in dividing_cells:
      changes = self.divide(dividing_cell)
      self.handleChangeInCells(changes)

  def handleGrowingCells(self):
    growingCells = [cell for cell in self.cells.values() if cell.wantsGrow()]
    for growingCell in growingCells:
      if growingCell in self.cells.values(): # additional check if cell wasn't already merged
        cells_to_merge = growingCell.grow()
        if cells_to_merge is None:
          return
        changes = self.merge_cells(cells_to_merge)
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

  def merge_cells(self, cells_to_merge):
    new_cell = self.create_new_cell(cells_to_merge)
    self.put_new_cell_into_neighbourhood(new_cell, cells_to_merge)
    return cells_to_merge, [new_cell]

  def create_new_cell(self, cells_to_merge):
    new_cell = VariableSquareCell.createInitialized(self.rule, self.neighbourhood)
    new_cell.position = self.interpolate_center(cells_to_merge)
    new_cell.size = len(cells_to_merge)*cells_to_merge[0].size
    new_cell.radius = cells_to_merge[0].radius*2
    return new_cell

  def put_new_cell_into_neighbourhood(self, new_cell, cells_to_merge):
    self.set_neighbours_of_new_cell(new_cell, cells_to_merge)
    self.update_surrounding_neighbourhood(new_cell, cells_to_merge)

  def set_neighbours_of_new_cell(self, new_cell, cells_to_merge):
    new_neighbours = self.neighbourhood.create_empty()
    for direction in new_neighbours.keys():
      new_neighbours[direction] = set([neigh for cell in cells_to_merge for neigh in cell.neighs[direction] if neigh not in cells_to_merge])
    new_cell.set_neighbours(new_neighbours)

  def update_surrounding_neighbourhood(self, new_cell, cells_to_merge):
    for direction, neighs in new_cell.neighs.items():
      for neigh in neighs:
        self.remove_old_neighbors(neigh, direction, cells_to_merge)
        self.add_new_neighbors(neigh, direction, [new_cell])

  @staticmethod
  def remove_old_neighbors(cell, direction, cells_to_remove):
    opposite_direction = VariableSquareLattice.reverse_direction(direction)
    for old_neigh in cells_to_remove:
      if old_neigh in cell.neighs[opposite_direction]:
        cell.neighs[opposite_direction].remove(old_neigh)

  @staticmethod
  def add_new_neighbors(cell, direction, cells_to_add):
    opposite_direction = VariableSquareLattice.reverse_direction(direction)
    cell.neighs[opposite_direction].update(cells_to_add)

  def divide(self, cell):
    # create 4 new cells
    cellNW = VariableSquareCell.createInitialized(self.rule, self.neighbourhood)
    cellNE = VariableSquareCell.createInitialized(self.rule, self.neighbourhood)
    cellSW = VariableSquareCell.createInitialized(self.rule, self.neighbourhood)
    cellSE = VariableSquareCell.createInitialized(self.rule, self.neighbourhood)

    cellNW.size = cell.size/4
    cellNE.size = cell.size/4
    cellSW.size = cell.size/4
    cellSE.size = cell.size/4

    # position
    half_radius = cell.radius/2

    cellNW.position = (cell.x - half_radius, cell.y - half_radius)
    cellNW.radius = half_radius
    cellNE.position = (cell.x + half_radius, cell.y - half_radius)
    cellNE.radius = half_radius
    cellSW.position = (cell.x - half_radius, cell.y + half_radius)
    cellSW.radius = half_radius
    cellSE.position = (cell.x + half_radius, cell.y + half_radius)
    cellSE.radius = half_radius

    # create neighbor connections
    cellNW.neighs["south"] = set([cellSW])
    cellNW.neighs["east"] = set([cellNE])
    cellNE.neighs["south"] = set([cellSE])
    cellNE.neighs["west"] = set([cellNW])
    cellSW.neighs["north"] = set([cellNW])
    cellSW.neighs["east"] = set([cellSE])
    cellSE.neighs["north"] = set([cellNE])
    cellSE.neighs["west"] = set([cellSW])

    new_cells = {}
    new_cells["north"] = [cellNW, cellNE]
    new_cells["east"] = [cellNE, cellSE]
    new_cells["south"] = [cellSE, cellSW]
    new_cells["west"] = [cellNW, cellSW]

    for direction, direction_neighs in cell.neighs.items():
      for direction_neigh in direction_neighs:
        for new_cell in new_cells[direction]:
          if self.is_neighbor_with(direction_neigh, new_cell):
            new_cell.neighs[direction].add(direction_neigh)

    # now we have new cells with correct neighs.
    # this time we have to update rest of the neighborhood
    for newCell in [cellNW, cellNE, cellSW, cellSE]:
      self.update_surrounding_neighbourhood(newCell, [self])

    return [cell], [cellNW, cellNE, cellSW, cellSE]

  @staticmethod
  def is_neighbor_with(cell1, cell2):
    cell1_left = cell1.x - cell1.radius
    cell1_right = cell1.x + cell1.radius
    cell2_left = cell2.x - cell2.radius
    cell2_right = cell2.x + cell2.radius

    cell1_top = cell1.y - cell1.radius
    cell1_bottom = cell1.y + cell1.radius
    cell2_top = cell2.y - cell2.radius
    cell2_bottom = cell2.y + cell2.radius

    if cell1_left < cell2_left or cell2_right < cell1_left:
      return False
    elif cell1_bottom < cell2_top or cell2_bottom < cell1_top:
      return False
    return True

  @staticmethod
  def interpolate_center(cells):
    one = cells[0]
    opposite = cells[2]
    x = (one.x + opposite.x) / 2
    y = (one.y + opposite.y) / 2
    return x,y

  @staticmethod
  def turn_right(direction):
    if direction == "north":
      return "east"
    elif direction == "east":
      return "south"
    elif direction == "south":
      return "west"
    elif direction == "west":
      return "north"
    else:
      raise Exception( direction + " is wrong direction to turn right!")

  @staticmethod
  def reverse_direction(direction):
    if direction == "north":
      return "south"
    elif direction == "east":
      return "west"
    elif direction == "south":
      return "north"
    elif direction == "west":
      return "east"
    else:
      raise Exception(direction + " is wrong direction to reverse!")

