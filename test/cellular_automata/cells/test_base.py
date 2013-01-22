from cellular_automata.cells.base import Cell
from cellular_automata.rules.base import DummyRule
import unittest

class CellTestCase(unittest.TestCase):
  def setUp(self):
    self.rule = DummyRule()
    self.cell = Cell(self.rule)

  def test_initial_position_of_created_cell(self):
    defaultPosition = (0,0)
    self.assertEqual(self.cell.position, defaultPosition)

  def test_cells_position_property_assignment(self):
    position = (3,4)
    self.cell.position = position
    self.assertEqual(self.cell._position, position)

  def test_cells_x_property_assignment(self):
    self.cell.x = 1
    self.assertEqual(self.cell._position, (1,0))

  def test_cells_y_property_assignment(self):
    self.cell.y = 1
    self.assertEqual(self.cell._position, (0,1))

  def test_cells_x_property_read(self):
    self.cell._position = (3,4)
    self.assertEqual(self.cell.x, 3)

  def test_cells_y_property_read(self):
    self.cell._position = (3,4)
    self.assertEqual(self.cell.y, 4)
