import sys
import os

ca_directory = os.getcwd()
if ca_directory not in sys.path:
    sys.path.insert(0, ca_directory)

from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.automaton.creator import get_conf

SUPPORTED_STATES = ["rgb", "color", "grayscale", "chemicals", "internal",
                    "alive", "binary"]


class Simulation(object):
    def __init__(self, conf_file=None):
        self.conf_file = conf_file
        if conf_file in None:
            # we have to initialize GUI and ask what to load CONF or LATTICE
            pass
        else:
            # create lattice widget(lw) subclass
            self.path_lattice_widget()

            # fire up GUI with this lattice widget subclass
            pass

    def path_lattice_widget(self):
        state_to_color, color_to_state = self.smart_state_mapping()
        LatticeWidget.map_state_to_rgb = state_to_color
        LatticeWidget.set_cell_state = color_to_state

    def smart_state_mapping(self):
        # get sample state
        sample_state = self.get_state_instance()

        for state in SUPPORTED_STATES:
            if hasattr(sample_state, state):
                state_to_color = self.create_color_mapping(getattr(
                    sample_state, state), state)
                color_to_state = self.create_state_mapping()
                break
        return state_to_color, color_to_state

    def create_state_mapping(self):
        pass

    def create_color_mapping(self, value, state_type):
        length = 1
        try:
            length = len(value)
        except TypeError as e:
            print("value {} is probably float or int".format(value))
            print("mapping to grayscale")
        else:
            length = 1

        if length == 1:
            return self.create_mapping("#{val:02X}{val:02X}{val:02X}",
                                       state_type)
        else:
            return self.create_mapping("#{:02X}{:02X}{:02X}", state_type)

    @staticmethod
    def create_mapping(mapping_string, attr_name):
        def map_state_to_rgb(self, state):
            return mapping_string.format(val=getattr(state, attr_name))
        return map_state_to_rgb

    def get_state_instance(self):
        conf = get_conf(self.conf_file)
        state_class = conf["state"]
        return state_class.create_state()
