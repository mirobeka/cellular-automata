from cPickle import Unpickler
import logging

log = logging.getLogger("LATTICE_BASE")


class Lattice:
    def __init__(self):
        self.width = self.height = 0
        self.age = 0
        self.chaotic = False

    def next_step(self):
        # go over all cells and perform next step
        raise NotImplementedError("method next_step of Lattice not implemented")

    @classmethod
    def read_border(cls, conf):
        """Transform setting of border from human readable to dictionary

        :param conf: lattice configuration in dictionary
        :return: dictionary with border cells values
        """
        border_top = eval(conf["borders"]["border_top"])
        border_left = eval(conf["borders"]["border_left"])
        border_right = eval(conf["borders"]["border_right"])
        border_bottom = eval(conf["borders"]["border_bottom"])

        border_top_northwest = eval(conf["borders"]["border_top_northwest"])
        border_top_northeast = eval(conf["borders"]["border_top_northeast"])

        border_left_northwest = eval(conf["borders"]["border_left_northwest"])
        border_left_southwest = eval(conf["borders"]["border_left_southwest"])

        border_right_northeast = eval(conf["borders"]["border_right_northeast"])
        border_right_southeast = eval(conf["borders"]["border_right_southeast"])

        border_bottom_southwest = eval(conf["borders"]["border_bottom_southwest"])
        border_bottom_southeast = eval(conf["borders"]["border_bottom_southeast"])

        resolution = int(conf["lattice"]["resolution"])

        width = int(conf["lattice"]["width"])
        height = int(conf["lattice"]["height"])

        border = dict()

        # TODO: reafctor this code please... pretty please :'(
        for x in xrange(0, width, resolution):

            coords_top = (x + resolution / 2, resolution / 2)
            coords_bottom = (x + resolution / 2, height - resolution / 2)

            border[coords_top] = {}
            border[coords_top]["north"] = border_top[x / resolution]
            border[coords_top]["northeast"] = border_top_northeast[x / resolution]
            border[coords_top]["northwest"] = border_top_northwest[x / resolution]
            border[coords_bottom] = {}
            border[coords_bottom]["south"] = border_bottom[x / resolution]
            border[coords_bottom]["southeast"] = border_bottom_southeast[x / resolution]
            border[coords_bottom]["southwest"] = border_bottom_southwest[x / resolution]

        for y in xrange(0, height, resolution):

            coords_left = (resolution / 2, y + resolution / 2)
            coords_right = (width - resolution / 2, y + resolution / 2)

            if coords_left not in border:
                border[coords_left] = {}
            border[coords_left]["west"] = border_left[y / resolution]
            border[coords_left]["northwest"] = border_left_northwest[y / resolution]
            border[coords_left]["southwest"] = border_left_southwest[y / resolution]
            if coords_right not in border:
                border[coords_right] = {}
            border[coords_right]["east"] = border_right[y / resolution]
            border[coords_right]["northeast"] = border_right_northeast[y / resolution]
            border[coords_right]["southeast"] = border_right_southeast[y / resolution]

        return border

    @classmethod
    def create_initialized(cls, conf):
        """Create and initialize lattice"""
        raise NotImplementedError(
            "create_initialized method of lattice not implemented")

    @classmethod
    def create_empty(cls):
        lattice = cls()
        return lattice

    @classmethod
    def load_configuration(cls, file_name):
        """ Unpickle lattice configuration from file"""
        with open(file_name, 'r') as f:
            upkl = Unpickler(f)
            lattice = upkl.load()
        if lattice is None:
            print("failed to unpickle or something else happened")
        return lattice

