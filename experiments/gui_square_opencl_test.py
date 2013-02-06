import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory) # adds path to cellular automata package

from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.equiangular import SquareLatticeCL
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.rules.neural_rule import ANNColorRule
from cellular_automata.rules.opencl_ready import MLPRule
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.visualization.tkinter_visualization import SimpleGUI
from cellular_automata.states.base import ChemicalInternalGrayscaleState
from Tkinter import Tk
import tkColorChooser
import yaml
import numpy as np

class SquareLatticeWidget(LatticeWidget):
  def map_state_to_rgb(self, state):
    return "#{val:02X}{val:02X}{val:02X}".format(val=state[0])

  def set_cell_state(self, event):
    item_id = self.find_closest(event.x, event.y)[0]
    cell = self.lattice.canvas_item_ids[item_id]
    rgb,color_hex = tkColorChooser.askcolor("white", title="choose cells state")
    if rgb is None:
      return
    self.itemconfig(item_id, fill=color_hex)
    cell.state.grayscale = rgb[0]

class GUISquareLatticeTest(SimpleGUI):
  def initialize_lattice(self):
    dimensions = (512, 512)
    rule = MLPRule()
    self.lattice = SquareLatticeCL.create_initialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=8,
        state=ChemicalInternalGrayscaleState,
        rule=rule)

if __name__ == "__main__":
  root = Tk()
  root.wm_title("Developmental experiment")
  test = GUISquareLatticeTest(root, SquareLatticeWidget)
  test.mainloop()



