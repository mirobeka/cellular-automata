class Lattice:
    def __init__(self):
        self.width = self.height = 0
        self.time = 0
        self.chaotic = False

    def next_step(self):
        # go over all cells and perform next step
        raise NotImplementedError("method next_step of Lattice not implemented")

    @classmethod
    def create_initialized(cls, conf):
        """Create and initialize lattice"""
        raise NotImplementedError(
            "create_initialized method of lattice not implemented")

    @classmethod
    def create_empty(cls):
        lattice = cls()
        return lattice
