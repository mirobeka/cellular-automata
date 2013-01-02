from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.rules.base import DummyRule
from cellular_automata.cells.regullar import VariableSquareCell
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
import unittest

class VariableSquareLatticeTestCase(unittest.TestCase):
  def setUp(self):
    self.rule = DummyRule()

  def test_cell_count_after_creation(self):
    lattice = VariableSquareLattice((2,2), vonNeumannNeighborhood, self.rule)
    self.assertEqual(4, len(lattice.cells))

  def test_cell_count_after_growing(self):
    lattice = VariableSquareLattice((2,2), vonNeumannNeighborhood, self.rule)
    for cell in lattice.cells:
      cell.setState([0,0,0,1])
    lattice.handleGrowingCells()
    self.assertEqual(1, len(lattice.cells))
