import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import EdieMoore
from cellular_automata.rules.game_of_life_rule import GameOfLifeRule
from cellular_automata.states.base import BinaryState
from cellular_automata.visualization.pygame_visualization import PygameVisualization

class GameOfLifeVisualization(PygameVisualization):
  def draw_cell(self, cell):
    tlx = cell.x - cell.radius
    tly = cell.y - cell.radius
    width = cell.radius*2
    height = cell.radius*2
    if cell.state.alive:
      py_color = self.white
    else:
      py_color = self.black
    self.draw_rect(py_color,(tlx, tly, width, height))

class GameOfLifeTest:
  def __init__(self):
    self.initialize_lattice()
    self.initialize_visualization()

  def initialize_lattice(self):
    dimensions = (1024,512)
    rule = GameOfLifeRule()
    self.lattice = SquareLattice.create_initialized(
        dimensions=dimensions,
        neighbourhood=EdieMoore,
        resolution=16,
        state=BinaryState,
        rule=rule)

  def initialize_visualization(self):
    self.vis = GameOfLifeVisualization(self.lattice)

  def initial_configuration(self, initial_configuration):
    for state,x,y in initial_configuration:
      state = BinaryState.create_state()
      state.alive = True
      self.lattice.set_state_of_cell(state,x,y)

  def start(self):
    self.vis.start()

if __name__ == "__main__":
  test = GameOfLifeTest()
  # glider_gun = [
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
  # test.initial_configuration(glider_gun)
  test.initial_configuration(conf)
  test.start()

