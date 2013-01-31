from cellular_automata.rules.base import Rule
from random import random

class StochasticRule(Rule):
  def get_next_state(self, cell, neighbours):
    number_of_living_neighbours = self.neighbours_alive(neighbours)
    probability = number_of_living_neighbours/10.0
    probability += 0.2
    new_state = cell.state.create_state()
    if random() <= probability:
      new_state.alive = True
    return new_state

  def neighbours_alive(self, neighs):
    # neighs is dictionary. key = direction (e.g. "north"), values = set of cells instances
    return sum([iter(neigh).next().state.alive for neigh in neighs.values() if len(neigh) == 1])
