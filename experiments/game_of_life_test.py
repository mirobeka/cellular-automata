import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighborhoods import edieMooreNeighborhood
from cellular_automata.rules.game_of_life_rule import GameOfLifeRule
from cellular_automata.visualization.base import PygameVisualization

class GameOfLifeVisualization(PygameVisualization):
  def drawCell(self, cell):
    tlx = cell.x - cell.radius
    tly = cell.y - cell.radius
    width = cell.radius*2
    height = cell.radius*2
    if cell.state == 0:
      pyColor = self.white
    else:
      pyColor = self.black
    self.drawRect(pyColor,(tlx, tly, width, height))

class GameOfLifeTest:
  def __init__(self):
    self.initializeLattice()
    self.initializeVisualization()

  def initializeLattice(self):
    dimensions = (1024,512)
    rule = GameOfLifeRule()
    self.lattice = SquareLattice.createInitialized(dimensions=dimensions, neighbourhoodMethod=edieMooreNeighborhood, resolution=16, rule=rule)

  def initializeVisualization(self):
    self.vis = GameOfLifeVisualization(self.lattice)

  def initialConfiguration(self, initialConfiguration):
    map(lambda (state,x,y): self.lattice.setStateOfCell(state,x,y), initialConfiguration)

  def start(self):
    self.vis.start()

if __name__ == "__main__":
  test = GameOfLifeTest()
  # gliderGun = [
  #     (1,24,2), (1,22,3), (1,24,3), (1,12,4), (1,13,4),
  #     (1,20,4), (1,21,4), (1,34,4), (1,35,4), (1,11,5),
  #     (1,15,5), (1,20,5), (1,21,5), (1,34,5), (1,35,5),
  #     (1,0,6),  (1,1,6),  (1,10,6), (1,16,6), (1,20,6),
  #     (1,21,6), (1,0,7),  (1,1,7),  (1,10,7), (1,14,7),
  #     (1,16,7), (1,17,7), (1,22,7), (1,24,7), (1,10,8),
  #     (1,16,8), (1,24,8), (1,11,9), (1,15,9), (1,12,10),
  #     (1,13,10)
  # ]
  conf = [
      (1,16,16), (1,16,32),
      (1,32,16), (1,32,32)
    ]
  # test.initialConfiguration(gliderGun)
  test.initialConfiguration(conf)
  test.start()

