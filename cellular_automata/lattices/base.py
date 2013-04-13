class Lattice:
    def __init__(self):
        self.width = self.height = 0
        self.time = 0
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
        border_top = eval(conf["border_top"])
        border_left = eval(conf["border_left"])
        border_right = eval(conf["border_right"])
        border_bottom = eval(conf["border_bottom"])
        resolution = int(conf["resolution"])
        width = int(conf["width"])
        height = int(conf["height"])

        border = dict()

        # TODO: reafctor this code please... pretty please :'(
        for x in xrange(0, width, resolution):
            coords_top = (x + resolution / 2, resolution / 2)
            coords_bottom = (x + resolution / 2, height - resolution / 2)
            if coords_top in border:
                border[coords_top]["n"] = border_top[x / resolution]
            else:
                border[coords_top] = {"n": border_top[x / resolution]}

            if coords_bottom in border:
                border[coords_bottom]["s"] = border_bottom[x / resolution]
            else:
                border[coords_bottom] = {"n": border_top[x / resolution]}

        for y in xrange(0, height, resolution):
            coords_left = (resolution / 2, y + resolution / 2)
            coords_right = (width - resolution / 2, y + resolution / 2)
            if coords_left in border:
                border[coords_left]["w"] = border_left[y / resolution]
            else:
                border[coords_left] = {"w": border_left[y / resolution]}

            if coords_right in border:
                border[coords_right]["e"] = border_right[y / resolution]
            else:
                border[coords_right] = {"e": border_right[y / resolution]}

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
