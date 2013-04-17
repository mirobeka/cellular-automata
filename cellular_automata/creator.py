from cellular_automata.lattices.base import Lattice
from utils.loader import get_conf


def create_automaton(conf_file):
    """ Loads configuration file and creates lattice based on parameters
    :param conf_file: config file describing cellular automata
    :return: lattice instance
    """
    conf = get_conf(conf_file)
    lattice_class = conf["simulation"]["lattice"]
    lattice = lattice_class.create_initialized(conf["simulation"])
    return lattice


def load_automaton(lattice_file):
    lattice = Lattice.load_configuration(lattice_file)
    return lattice
