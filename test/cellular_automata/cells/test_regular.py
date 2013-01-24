from cellular_automata.cells.regular import SquareCell
from cellular_automata.cells.regular import VariableSquareCell
from cellular_automata.rules.base import DummyRule
from cellular_automata.rules.base import AllwaysMergeRule
from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
import unittest

class SquareCellTestCase(unittest.TestCase):
  def setUp(self):
    self.rule = DummyRule()
    self.cell = SquareCell(self.rule)

  def test_cell_export_to_dictionary(self):
    c1 = SquareCell(self.rule)
    c1.position = (23, 47)
    c2 = SquareCell(self.rule)
    c2.position = (2, 5)
    c3 = SquareCell(self.rule)
    c3.position = (90, 4)
    c4 = SquareCell(self.rule)
    c4.position = (3, 7)

    self.cell.neighs["north"] = set([c1, c2])
    self.cell.neighs["east"] = set([c2])
    self.cell.neighs["south"] = set([c3])
    self.cell.neighs["west"] = set([c4])

    resultDictionary = {
          'state': 0,
          'north': set([(23, 47), (2, 5)]),
          'east': set([(2,5)]),
          'south': set([(90, 4)]),
          'west': set([(3, 7)]),
          'northeast': set([]),
          'southeast': set([]),
          'southwest': set([]),
          'northwest': set([])
        }
    self.assertDictEqual(self.cell.toDict(), resultDictionary)

class VSCTestCase(unittest.TestCase):
  def latticeStateInitialization(self, lattice, initialStates):
    for idx,initialState in enumerate(initialStates):
      lattice.cells[idx].setState(initialState)
    return lattice

  def createLattice(self, size, configuration, rule = DummyRule()):
    lattice = VariableSquareLattice((size, size), vonNeumannNeighborhood, rule)
    lattice = self.latticeStateInitialization(lattice, configuration)
    return lattice

  def createEmptyNeighborhood(self):
    neighs = {}
    neighs["northeast"] = set()
    neighs["southeast"] = set()
    neighs["northwest"] = set()
    neighs["southwest"] = set()
    neighs["south"] = set()
    neighs["east"] = set()
    neighs["north"] = set()
    neighs["west"] =  set()
    return neighs

class VariableSquareCellHelperMethodsTestCase(VSCTestCase):
  '''Unit test for variable square cell's helper methods'''
  def setUp(self):
    self.rule = DummyRule()
    self.cell = VariableSquareCell(self.rule)

  def test_ok_to_redirect_north_to_south(self):
    self.assertEqual('south', self.cell.reverseDirection('north'))

  def test_ok_to_redirect_east_to_west(self):
    self.assertEqual('west', self.cell.reverseDirection('east'))

  def test_ok_to_redirect_west_to_east(self):
    self.assertEqual('east', self.cell.reverseDirection('west'))

  def test_ok_to_redirect_south_to_north(self):
    self.assertEqual('north', self.cell.reverseDirection('south'))

  def test_ok_to_turn_north_to_east_direction(self):
    self.assertEqual('east', self.cell.turnRight('north'))

  def test_ok_to_turn_north_to_east_direction(self):
    self.assertEqual('south', self.cell.turnRight('east'))

  def test_ok_to_turn_north_to_east_direction(self):
    self.assertEqual('west', self.cell.turnRight('south'))

  def test_ok_to_turn_north_to_east_direction(self):
    self.assertEqual('north', self.cell.turnRight('west'))

class VariableSquareCellNeighborhoodTestCase(VSCTestCase):
  '''Unit test for Variable Square Cell merging and neighborhood methods'''
  def setUp(self):
    self.rule = DummyRule()
    self.lattice = self.createLattice(3, [
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]
      ])
    self.center = self.lattice.cells[4]
    self.north = self.lattice.cells[1]
    self.northEast = self.lattice.cells[2]
    self.east = self.lattice.cells[5]
    self.southEast = self.lattice.cells[8]
    self.south = self.lattice.cells[7]
    self.southWest = self.lattice.cells[6]
    self.west = self.lattice.cells[3]
    self.northWest = self.lattice.cells[0]

  def test_north_neighbor_after_initialization_of_lattice(self):
    northNeighborhood = self.center.neighs["north"]
    self.assertIn(self.north, northNeighborhood)

  def test_west_neighbor_after_initialization_of_lattice(self):
    westNeighborhood = self.center.neighs["west"]
    self.assertIn(self.west, westNeighborhood)

  def test_east_neighbor_after_initialization_of_lattice(self):
    eastNeighborhood = self.center.neighs["east"]
    self.assertIn(self.east, eastNeighborhood)

  def test_south_neighbor_after_initialization_of_lattice(self):
    southNeighborhood = self.center.neighs["south"]
    self.assertIn(self.south, southNeighborhood)

  def test_ok_can_merge_with_cells_that_wants_to_merge(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    self.assertTrue(self.center.canMergeWithOthers("north"))

  def test_fail_can_merge_with_north_cell_dont_grow(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,0,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    self.assertFalse(self.center.canMergeWithOthers("north"))

  def test_returns_correct_cells_to_merge(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    correctList = [self.center, self.north, self.northEast, self.east]
    self.assertListEqual(correctList, self.center.getCellsToMerge("north"))

  def test_new_cell_should_have_correct_north_neighborhood(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    cellsToMerge = [self.center, self.north, self.northEast, self.east]
    newCell = self.center.createNewCell(cellsToMerge)
    self.center.setNeighborsOfNewCell(newCell, cellsToMerge)
    self.assertSetEqual(set(), newCell.neighs["north"])

  def test_new_cell_should_have_correct_south_neighborhood(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    cellsToMerge = [self.center, self.north, self.northEast, self.east]
    newCell = self.center.createNewCell(cellsToMerge)
    self.center.setNeighborsOfNewCell(newCell, cellsToMerge)
    self.assertSetEqual(set([self.southEast, self.south]), newCell.neighs["south"])

  def test_new_cell_should_have_correct_west_neighborhood(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    cellsToMerge = [self.center, self.north, self.northEast, self.east]
    newCell = self.center.createNewCell(cellsToMerge)
    self.center.setNeighborsOfNewCell(newCell, cellsToMerge)
    self.assertSetEqual(set([self.west, self.northWest]), newCell.neighs["west"])

  def test_new_cell_should_have_correct_east_neighborhood(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    cellsToMerge = [self.center, self.north, self.northEast, self.east]
    newCell = self.center.createNewCell(cellsToMerge)
    self.center.setNeighborsOfNewCell(newCell, cellsToMerge)
    self.assertSetEqual(set(), newCell.neighs["east"])

  def test_size_of_new_cell_should_be_4(self):
    self.center.setState([0,0,0,1,0])
    self.north.setState([0,0,0,1,0])
    self.northEast.setState([0,0,0,1,0])
    self.east.setState([0,0,0,1,0])
    cellsToMerge = [self.center, self.north, self.northEast, self.east]
    newCell = self.center.createNewCell(cellsToMerge)
    self.assertEqual(4,newCell.size)

  def setNeighborsAsCenterCell(self, newCell):
    newCell.neighs["north"] = set([self.north])
    newCell.neighs["east"] = set([self.east])
    newCell.neighs["south"] = set([self.south])
    newCell.neighs["west"] = set([self.west])

  def test_update_north_neighbor_with_new_cell_in_neighborhood(self):
    newCell = VariableSquareCell(self.rule)
    self.setNeighborsAsCenterCell(newCell)
    self.center.updateNeighborhood(newCell, [self.center])
    self.assertIn(newCell, self.north.neighs["south"])

  def test_update_east_neighbor_with_new_cell_in_neighborhood(self):
    newCell = VariableSquareCell(self.rule)
    self.setNeighborsAsCenterCell(newCell)
    self.center.updateNeighborhood(newCell, [self.center])
    self.assertIn(newCell, self.east.neighs["west"])

  def test_update_south_neighbor_with_new_cell_in_neighborhood(self):
    newCell = VariableSquareCell(self.rule)
    self.setNeighborsAsCenterCell(newCell)
    self.center.updateNeighborhood(newCell, [self.center])
    self.assertIn(newCell, self.south.neighs["north"])

  def test_update_west_neighbor_with_new_cell_in_neighborhood(self):
    newCell = VariableSquareCell(self.rule)
    self.setNeighborsAsCenterCell(newCell)
    self.center.updateNeighborhood(newCell, [self.center])
    self.assertIn(newCell, self.west.neighs["east"])

class VariableSquareCellMergeTestCase(VSCTestCase):
  def setUp(self):
    self.rule = AllwaysMergeRule()
    self.lattice = self.createLattice(4, [
        [0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],
        [0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],
        [0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],
        [0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0]
      ], self.rule)

  def test_grid_of_16_cells_after_1_merge_pass_should_merge_into_4_cells(self):
    # after first merge, there should be just 4 cells
    self.lattice.handleGrowingCells()
    self.assertEqual(4, len(self.lattice.cells))

  def test_grid_of_16_cells_after_2_merge_pass_should_merge_into_1_cell(self):
    self.lattice.handleGrowingCells()
    map(lambda cell: cell.computeNextState(), self.lattice.cells)
    map(lambda cell: cell.applyNextState(), self.lattice.cells)
    self.lattice.handleGrowingCells()
    self.assertEqual(1, len(self.lattice.cells))

  def printLattice(self, lattice):
    print("\n\n\n\n\n==================== lattice {}".format(id(lattice)))
    map(lambda cell: self.printCell(cell), lattice.cells)
    print("\n\n\n\n")

  def printCell(self, cell):
    print("\nCell {}".format(id(cell)))
    print("Neighbors:")
    self.printNeighs(cell.neighs)
    print("Size: {}".format(cell.size))
    print("State: {}".format(cell.getState()))

  def printNeighs(self, neighs):
    for direction, neigh in neighs.items():
      print("{} => {}".format(direction, [id(n) for n in neigh]))

class VariableSquareCellSizeTestCase(unittest.TestCase):
  def setUp(self):
    self.rule = DummyRule()
    self.smallCell1 = VariableSquareCell(self.rule)
    self.smallCell2 = VariableSquareCell(self.rule)
    self.bigCell = VariableSquareCell(self.rule)
    self.bigCell.size = 4

  def test_fails_when_comparing_different_cell_sizes(self):
    self.assertFalse(self.smallCell1.sameSize(self.bigCell))

  def test_ok_when_comparing_same_sized_cells(self):
    self.assertTrue(self.smallCell1.sameSize(self.smallCell2))

