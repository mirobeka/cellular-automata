from cellular_automata.cells.regular import SquareCell
from cellular_automata.rules.base import DummyRule
import unittest

class SquareCellTestCase(unittest.TestCase):
  def setUp(self):
    self.rule = DummyRule(4)

  def test_SquareCell_default_state(self):
    cell = SquareCell(self.rule)

