import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory) # adds path to cellular automata package

from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.rules.neural_rule import ANNColorRule
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.visualization.tkinter_visualization import SimpleGUI
from cellular_automata.states.base import ChemicalInternalGrayscaleState
from Tkinter import Tk
import tkColorChooser
import yaml
import numpy as np

class SquareLatticeWidget(LatticeWidget):
  def map_state_to_rgb(self, state):
    return "#{val:02X}{val:02X}{val:02X}".format(val=state.grayscale)

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
    dimensions = (256, 256)
    rule = ANNColorRule()
    rule.set_weights(self.get_weights())
    self.lattice = SquareLattice.create_initialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=32,
        state=ChemicalInternalGrayscaleState,
        rule=rule)
  
  def get_weights(self):
    return np.array([
1.07420205255,1.57943915708,0.0699283759426,-3.78738402397,-0.064322422248,-1.24681460725,2.36579226916,2.66041013319,-0.21662416959,-0.0411580259544,0.0404915335676,2.04954283279,-1.00664098989,0.532149145626,1.73787262836,-0.199223392565,-0.589634166809,-1.45856020022,-0.107928580165,-0.605131911192,-0.065188344112,2.20325814586,0.555046188286,2.35536133195,3.72804098106,1.42463664442,-1.4777233237,0.955201783715,-1.75939691593,-1.76353710308,1.30456855567,-1.00683327244,1.65463578414,2.35651631417,0.683375376592,-3.37804141955,-1.04484444863,0.482764876246,0.268371559455,-0.278519370887,-1.09134013652,2.3660609252,1.55870202344,-0.685047374313,0.110006571515,-0.458546272012,-0.747226865748,-2.83431786491,1.93202433205,-0.673698619359,0.928846163838,-1.77306382267,1.04379649033,2.23587721382,0.554185075123,4.04647343344,1.11548964793,-0.495191762772,-0.525733885113,-0.501636739917,1.46273681976,0.39069172367,-0.0780916984308,-1.15121932924,-1.14248185229,2.51662534406,1.85468617117,-0.173232376523,1.2013157753,-0.955750939169,0.937949935919,-2.1336960562,0.766431598034,2.79506911567,-0.580767983501,0.940760231963,-2.86273030494,0.565048499815,2.31736868222,1.43928293279,2.77913704689,0.00116822793137,1.00599804499,0.000150824467045
])

if __name__ == "__main__":
  root = Tk()
  root.wm_title("Developmental experiment")
  test = GUISquareLatticeTest(root, SquareLatticeWidget)
  test.mainloop()


