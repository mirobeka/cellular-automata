class Lattice:
  def __init__(self):
    self.width = self.height = 0
    self.time = 0

  def next_step(self):
    # go over all cells and perform next step
    raise NotImplementedError("method next_step of Lattice not implemented")

  @classmethod
  def read_from_file(cls, filename):
    raise NotImplementedError("read_file method of lattice not implemented")

  def save_to_file(self, filename):
    '''Saves configuration of instance of lattice in file'''
    raise NotImplementedError("save_to_file method of lattice not implemented")

  @classmethod
  def create_initialzed(cls, **kwargs):
    '''Create and initialize lattice'''
    raise NotImplementedError("create_initialized method of lattice not implemented")

  @classmethod
  def create_empty(cls):
    lattice = cls()
    return lattice
