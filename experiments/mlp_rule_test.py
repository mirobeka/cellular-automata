import sys
sys.path.insert(0,"/Users/miroslavbeka/Development/CA/")
print(sys.path)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
from cellular_automata.rules.neural_rule import MLPRule
from cellular_automata.visualization.base import PygameVisualization

import pygame, sys
from pygame.locals import *

black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)

class MLPTest:
  def __init__(self):
    self.initializeLattice()
    self.initializeVisualization()

  def initializeVisualization(self):
    self.vis = PygameVisualization(self.lattice)

  def initializeLattice(self):
    dimensions = (16,16)
    rule = MLPRule()
    self.lattice = VariableSquareLattice(dimensions, vonNeumannNeighborhood, rule)
    
  def start(self):
    self.vis.start()

if __name__ == "__main__":
  test = MLPTest()
  test.start()
