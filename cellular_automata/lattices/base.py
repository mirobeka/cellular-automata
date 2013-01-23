class Lattice:
  def nextStep(self):
    # go over all cells and perform next step
    raise NotImplementedError("method nextStep of Lattice not implemented")

  @classmethod
  def loadFromFile(cls, filename):
    '''Load configuration of lattice form file and creates new lattice'''
    configuration = cls.readFile(filename)
    cls.createFromConfiguration(configuration)

  @classmethod
  def readFromFile(cls, filename):
    raise NotImplementedError("readFile method of lattice not implemented")

  def saveToFile(self, filename):
    '''Saves configuration of instance of lattice in file'''
    raise NotImplementedError("saveToFile method of lattice not implemented")

  @classmethod
  def createInitialzed(cls, **kwargs):
    '''Create and initialize lattice'''
    raise NotImplementedError("createInitialized method of lattice not implemented")

  @classmethod
  def createEmpty(cls):
    lattice = cls()
    return lattice
