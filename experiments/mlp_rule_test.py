import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.rules.neural_rule import MLPColorTopologyRule
from cellular_automata.visualization.pygame_visualization import PygameVisualization
from cellular_automata.states.base import ColorTopologyState

class MLPTest:
  def __init__(self):
    self.initializeLattice()
    self.initializeVisualization()

  def initializeVisualization(self):
    self.vis = PygameVisualization(self.lattice)

  def initializeLattice(self):
    dimensions = (256,256)
    rule = MLPColorTopologyRule()
    self.lattice = VariableSquareLattice.createInitialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=16,
        state=ColorTopologyState,
        rule=rule)
    
  def start(self):
    self.vis.start()

if __name__ == "__main__":
  test = MLPTest()
  test.start()
