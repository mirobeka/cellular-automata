from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.rules.base import DummyRule
from cellular_automata.cells.regular import VariableSquareCell
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
import unittest

class VariableSquareLatticeTestCase(unittest.TestCase):
  '''Unit Test for variable square lattice'''
  def setUp(self):
    self.rule = DummyRule()

  def latticeStateInitialization(self, lattice, initialStates):
    for idx,initialState in enumerate(initialStates):
      lattice.cells[idx].setState(initialState)
    return lattice

  def createLattice(self, size, configuration):
    lattice = VariableSquareLattice((size, size), vonNeumannNeighborhood, self.rule)
    lattice = self.latticeStateInitialization(lattice, configuration)
    return lattice

  def createBasicLattice(self, dimension):
    lattice = VariableSquareLattice((dimension, dimension), vonNeumannNeighborhood, self.rule)
    return lattice

  def test_cell_count_after_creation(self):
    lattice = self.createBasicLattice(2)
    self.assertEqual(4, len(lattice.cells))

  def test_cell_count_after_growing(self):
    lattice = self.createLattice(2,[
        [0,0,0,1],[0,0,0,1],
        [0,0,0,1],[0,0,0,1]
      ])
    lattice.handleGrowingCells()
    self.assertEqual(1, len(lattice.cells))

  def test_cell_count_after_complex_growing(self):
    initialStates = [
          [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],
          [0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],
          [0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],
          [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]
        ]
    lattice = self.createLattice(4, initialStates)
    lattice.handleGrowingCells()
    self.assertEqual(13, len(lattice.cells))

  def test_cell_size_should_be_4_after_merge(self):
    lattice = self.createLattice(2,[
        [0,0,0,1],[0,0,0,1],
        [0,0,0,1],[0,0,0,1]
      ])
    lattice.handleGrowingCells()
    cell = lattice.cells[0]
    self.assertEqual(4, cell.size)

  def test_cell_count_stays_same_after_failed_merge(self):
    lattice = self.createLattice(2,[
        [0,0,0,0],[0,0,0,0],
        [0,0,0,0],[0,0,0,0]
      ])
    lattice.handleGrowingCells()
    self.assertEqual(4, len(lattice.cells))

  def test_cell_center_position_after_merge(self):
    self.assertTrue(False)

  def test_should_fail_to_merge_cells(self):
    lattice = self.createBasicLattice(2)
    lattice.handleGrowingCells()
    self.assertEqual(4, len(lattice.cells))

