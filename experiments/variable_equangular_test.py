import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
from cellular_automata.rules.base import DummyRule
from cellular_automata.visualization.base import PygameVisualization
import pygame

class VariableSquareLatticeVisualization(PygameVisualization):
  def drawCell(self, cell):
    tlx = cell.x - cell.radius
    tly = cell.y - cell.radius
    width = cell.radius*2
    height = cell.radius*2
    if cell.size == 1:
      pyColor = pygame.color.Color(cell.state[0],0,0)
    elif cell.size == 4:
      pyColor = pygame.color.Color(0,cell.state[1],0)
    else:
      pyColor = pygame.color.Color(0,0,cell.state[2])
    self.drawRect(pyColor,(tlx, tly, width, height))

class VariableSquareLatticeTest:
  def __init__(self):
    self.initializeLattice()
    self.initializeVisualization()

  def initializeLattice(self):
    dimensions = (256, 256)
    rule = DummyRule()
    self.lattice = VariableSquareLattice.createInitialized(
        dimensions=dimensions, 
        neighbourhoodMethod=vonNeumannNeighborhood,
        resolution=16,
        rule=rule)

  def initializeVisualization(self):
    self.vis = VariableSquareLatticeVisualization(self.lattice)

  def start(self):
    self.vis.start()

if __name__ == "__main__":
  test = VariableSquareLatticeTest()
  test.start()
