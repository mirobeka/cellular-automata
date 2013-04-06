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
import numpy as np


class SquareLatticeWidget(LatticeWidget):
    def map_state_to_rgb(self, state):
        return "#{val:02X}{val:02X}{val:02X}".format(val=state.grayscale)

    def set_cell_state(self, event):
        item_id = self.find_closest(event.x, event.y)[0]
        cell = self.lattice.canvas_item_ids[item_id]
        rgb, color_hex = tkColorChooser.askcolor("white",
                                                 title="choose cells state")
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
            resolution=64,
            state=ChemicalInternalGrayscaleState,
            rule=rule)

    def get_weights(self):
        # return  np.array([1]*84)
        return np.array([
            1.07420205255, 1.57943915708, 0.0699283759426, -3.78738402397,
            -0.064322422248, -1.24681460725, 2.36579226916, 2.66041013319,
            -0.21662416959, -0.0411580259544, 0.0404915335676, 2.04954283279,
            -1.00664098989, 0.532149145626, 1.73787262836, -0.199223392565,
            -0.589634166809, -1.45856020022, -0.107928580165, -0.605131911192,
            -0.065188344112, 2.20325814586, 0.555046188286, 2.35536133195,
            3.72804098106, 1.42463664442, -1.4777233237, 0.955201783715,
            -1.75939691593, -1.76353710308, 1.30456855567, -1.00683327244,
            1.65463578414, 2.35651631417, 0.683375376592, -3.37804141955,
            -1.04484444863, 0.482764876246, 0.268371559455, -0.278519370887,
            -1.09134013652, 2.3660609252, 1.55870202344, -0.685047374313,
            0.110006571515, -0.458546272012, -0.747226865748, -2.83431786491,
            1.93202433205, -0.673698619359, 0.928846163838, -1.77306382267,
            1.04379649033, 2.23587721382, 0.554185075123, 4.04647343344,
            1.11548964793, -0.495191762772, -0.525733885113, -0.501636739917,
            1.46273681976, 0.39069172367, -0.0780916984308, -1.15121932924,
            -1.14248185229, 2.51662534406, 1.85468617117, -0.173232376523,
            1.2013157753, -0.955750939169, 0.937949935919, -2.1336960562,
            0.766431598034, 2.79506911567, -0.580767983501, 0.940760231963,
            -2.86273030494, 0.565048499815, 2.31736868222, 1.43928293279,
            2.77913704689, 0.00116822793137, 1.00599804499, 0.000150824467045
            #       ANOTHER SET OF WEIGHTS
            # -7.82809865,2.34218097,7.6328322,6.11701076,-1.86128563,
            # -11.92830144, -0.29840854,3.12580255,-5.32558075,3.65081706,
            # 7.526405,10.75988755,-3.23483005,-7.55251134,0.63375546,
            # -0.80807388,11.29079085,-1.83897764,-16.25623617,2.79761763,
            # -7.90013886,13.28802361,-4.63730154,-1.25229073,-4.20567558,
            # 3.49961569,1.03497475,-3.67272485,-8.24136835,-8.5466071,
            # 18.03193365,-3.29357964,0.19010698,0.09880874,-4.2347923,
            # 9.86126953,1.23196789,-0.29709521,2.06584099,-9.92839725,
            # 4.16866048,5.07994545,-0.63080076,5.56043453,4.63944659,
            # -3.21800726,-7.80444815,-0.10814349,1.70560423,11.0676525,
            # 0.36508894,0.56848296,8.71106366,-2.66174672,6.11544252,
            # -2.3894302,7.72440283,0.45037174,12.64460271,4.21834871,
            # 4.13803811,7.86203628,-3.61703989,-0.63365374,2.60991585,
            # -5.85162872,-2.76470959,-5.453099,4.53986373,3.06693653,
            # 4.22843065,0.19378628,8.40573642,-0.15652506,7.11764143,
            # -5.6758835,-17.10335637,1.55964619,0.67882338,-5.69714116,
            # 3.14338246,6.91499342,16.23516148,-0.80319345
        ])


if __name__ == "__main__":
    root = Tk()
    root.wm_title("Developmental experiment")
    test = GUISquareLatticeTest(root, SquareLatticeWidget)
    test.mainloop()


