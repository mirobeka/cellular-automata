class Lattice:
  def nextStep(self):
    # go over all cells and perform next step
    raise NotImplementedError("method nextStep of Lattice not implemented")

  @classmethod
  def loadFromFile(cls, filename):
    '''
    load configuration of lattice, create cells, set cells states
    neighbours and other stuff

    this should be lattice specific, so this is just abstract class method
    '''
    raise NotImplementedError("Method loadFromFile of Lattice is not implemented")
    

  
