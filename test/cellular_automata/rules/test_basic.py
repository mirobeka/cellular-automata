from cellular_automata.rules.base import Rule
from cellular_automata.rules.base import DummyRule
from cellular_automata.rules.base import NotImplementedException
from cellular_automata.cells.base import Cell
import unittest

class BaseRuleTestCase(unittest.TestCase):
  '''Unit test for BaseRule class''' 
  def test_getNextState_exception(self):
    rule = Rule()
    self.assertRaises(NotImplementedException, rule.getNextState, None, None)

class DummyRuleTestCase(unittest.TestCase):
  '''Unit test for DummyRule class'''
  def test_default_state_vector_length_value(self):
    rule = DummyRule()
    self.assertEqual(4, rule.stateVectorLength)

