from cellular_automata.rules.base import Rule
from random import random

class StochasticRule(Rule):
  def __init__(self):
    Rule.__init__(self)

  def getNextState(self, cell, neighbours):
    number_of_living_neighbours = self.neighbours_alive(neighbours)
    probability = number_of_living_neighbours/.0
    probability += 0.2
    new_state = [0]*len(cell.state)
    if random() <= probability:
      new_state[0]=1
    return new_state

  def neighbours_alive(self, neighs):
    return sum([iter(neigh).next().state[0] for neigh in neighs.values() if len(neigh) == 1])

  def initialState(self):
    return [0]
