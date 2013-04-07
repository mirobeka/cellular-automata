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
        """ dynamically create method for mapping state of cell into color
        space and back from color into cell state. Method is created based on
         type of state variable and it's name.
        :return: tuple of methods state -> rgb, rgb -> state
        """
        sample_state = self.get_state_instance()

        for state in SUPPORTED_STATES:
            if hasattr(sample_state, state):
                state_to_color = self.create_color_mapping(getattr(
                    sample_state, state), state)
                color_to_state = self.create_state_mapping(getattr(
                    sample_state, state), state)
                break
        return state_to_color, color_to_state

    def create_state_mapping(self, value, state_type):
        """This method creates method that is used to override not
        implemented LatticeWidget method for mapping rgb color into cell state

        :param value: sample value of state variable. Just to know what type it is
        :param state_type: name of attribute of this state variable
        :return: method map_state_to_rgb
        """
        length = 1
        try:
            length = len(value)
        except TypeError:
            print("value {} is not tuple or list".format(value))
            print("mapping to grayscale")
        else:
            length = 1

        # this is super ugly, find better way to do this
        if length == 1:
            if type(value) is float:
                def map_rgb_to_state(self, rgb, state):
                    setattr(state, state_type, rgb[0]/255.0)
                return map_rgb_to_state
            else:
                def map_rgb_to_state(self, rgb, state):
                    setattr(state, state_type, rgb[0])
        else:
            if type(value[0]) is float:
                def map_rgb_to_state(self, rgb, state):
                    setattr(state, state_type, tuple([map(lambda x: x/255.0),
                                                      rgb]))
                return map_rgb_to_state
            else:
                def map_rgb_to_state(self, rgb, state):
                    setattr(state, state_type, rgb)
                return map_rgb_to_state

    def create_color_mapping(self, value, state_type):
        """This method creates method that is used to override not
        implemented LatticeWidget method for mapping state of cell into color
         space

        :param value: sample value of state variable. Just to know what type it is
        :param state_type: name of attribute of this state variable
        :return: method map_state_to_rgb
        """
        length = 1
        try:
            length = len(value)
        except TypeError as e:
            print("value {} is not tuple or list".format(value))
            print("mapping to grayscale")
        else:
            length = 1

        if length == 1:
            def map_state_to_rgb(self, state):
                return "#{val:02X}{val:02X}{val:02X}".format(val=getattr(
                    state, state_type))
            return map_state_to_rgb
        else:
            def map_state_to_rgb(self, state):
                return "#{:02X}{:02X}{:02X}".format(getattr(state, state_type))
            return map_state_to_rgb

    def get_state_instance(self):
        conf = get_conf(self.conf_file)
        state_class = conf["state"]
        return state_class.create_state()
