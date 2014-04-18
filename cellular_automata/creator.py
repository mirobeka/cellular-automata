from cellular_automata.lattices.base import Lattice
from utils.loader import get_conf
import logging

class LatticeMockup:
    def __init__(self, width, height, resolution):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.create_cells()

    def create_cells(self):
        raise NotImplementedError("Implement create_cells")

    def set_cells_state(self, data_string):
        data = eval(data_string)
        idx = 0
        for y in range(0, self.height, self.resolution):
            for x in range(0, self.width, self.resolution):
                self.cells[(x,y)] = data[idx]
                idx += 1

    @classmethod
    def create_mockup(cls, pattern_path):
        w = h = r = 0
        type=""
        try:
            with open(pattern_path, "r") as fp:
                w,h,r,type = fp.readline().strip().split(" ")
                w=int(w)
                h=int(h)
                r=int(r)
                string_array = fp.readlines()
        except IOError as e:
            log = loggin.getLogger("PATTERN")
            log.error("Error readling patter file")
            return None
        if type == "grayscale":
            mockup = GrayscaleLatticeMockup(w, h, r)
        else:
            mockup = RGBLatticeMockup(w, h, r)

        data_string = "".join(string_array)
        mockup.set_cells_state(data_string)

        return mockup

class GrayscaleLatticeMockup(LatticeMockup):
    def create_cells(self):
        self.cells = {}
        for x in range(0, self.width, self.resolution):
            for y in range(0, self.height, self.resolution):
                self.cells[(x, y)] = 0

class RGBLatticeMockup(LatticeMockup):
    def create_cells(self):
        self.cells = {}
        for x in range(0, self.width, self.resolution):
            for y in range(0, self.height, self.resolution):
                self.cells[(x, y)] = [0,0,0]

def create_automaton(conf_file):
    """ Loads configuration file and creates lattice based on parameters
    :param conf_file: config file describing cellular automata
    :return: lattice instance
    """
    conf = get_conf(conf_file)
    lattice_class = conf["lattice"]["type"]
    lattice = lattice_class.create_initialized(conf)
    return lattice

def load_automaton(lattice_file):
    lattice = Lattice.load_configuration(lattice_file)
    return lattice

def load_pattern(pattern_file):
    return LatticeMockup.create_mockup(pattern_file)
