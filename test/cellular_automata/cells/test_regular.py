from cellular_automata.cells.regular import SquareCell
from cellular_automata.cells.regular import VariableSquareCell
from cellular_automata.rules.base import DummyRule
from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
import unittest

class VariableSquareCellHelperMethodsTestCase(unittest.TestCase):
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

class VariableSquareCellNeighborhoodTestCase(unittest.TestCase):
  '''Unit test for Variable Square Cell merging and neighborhood methods'''
  def setUp(self):
    self.rule = DummyRule()
    self.lattice = self.createLattice(3, [
        [0,0,0,0],[0,0,0,0],[0,0,0,0],
        [0,0,0,0],[0,0,0,0],[0,0,0,0],
        [0,0,0,0],[0,0,0,0],[0,0,0,0]
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

  def latticeStateInitialization(self, lattice, initialStates):
    for idx,initialState in enumerate(initialStates):
      lattice.cells[idx].setState(initialState)
    return lattice

  def createLattice(self, size, configuration):
    rule = DummyRule()
    lattice = VariableSquareLattice((size, size), vonNeumannNeighborhood, rule)
    lattice = self.latticeStateInitialization(lattice, configuration)
    return lattice

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
    self.center.setState([0,0,0,1])
    self.north.setState([0,0,0,1])
    self.northEast.setState([0,0,0,1])
    self.east.setState([0,0,0,1])
    self.assertTrue(self.center.canMergeWithOthers("north"))

  def test_fail_can_merge_with_north_cell_dont_grow(self):
    self.center.setState([0,0,0,1])
    self.north.setState([0,0,0,0])
    self.northEast.setState([0,0,0,1])
    self.east.setState([0,0,0,1])
    self.assertFalse(self.center.canMergeWithOthers("north"))

  def test_returns_correct_cells_to_merge(self):
    self.center.setState([0,0,0,1])
    self.north.setState([0,0,0,1])
    self.northEast.setState([0,0,0,1])
    self.east.setState([0,0,0,1])
    correctList = [self.center, self.north, self.northEast, self.east]
    self.assertListEqual(correctList, self.center.getCellsToMerge("north"))

  # def test_correct_size_of_new_cell_after_merge(self):
  #   cellsToMerge = [self.center, self.north, self.northEast, self.east]
  #   self.center

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

