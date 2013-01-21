import sys, os
ca_directory = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

import cmaes.barecmaes2 as cma
from cellular_automata.lattices.eqiuangular import SquareLattice
from cellular_automata.lattices.neighbors import vonNeumannNeighborhood


class CmaesExperiment:
  '''
  Well this experiment needs:
    -> error function
    -> objective function which we try to minimize
    -> updating weights of neural network
    -> 
  '''
  def __init__(self):
    self.loadPredefinedLattice('data/two_band_configuration.ltc')

  def start(self):
    initialWeights = self.getInitialValues()
    result = cma.fmin(self.objective, initialWeights, 0.3, verb_disp=100)
    self.writeResult(result)

  def writeResult(self, result):
    pass

  def objective(self, networkWeights):
    '''
    prepare celluar automata to run
    set weights of rule or other thing what we evolve
    run cellular automata for some time or stop by some stop constraint
    return output of error function
    '''
    pass

  def error(self, lattice):
    '''
    here we have to check if color is in the right position
    so for all cells in two dimensional array of cells, go over each cell
    and compare it to predefined cells color
    
    later we should add also location, exact color, (neighbours)


    '''
    pass

  def loadPredefinedLattice(self, filename):
    self.predefinedLattice = SquareLattice.loadFromFile(filename)

if __name__ == "__main__":
  experiment = CmaesExperiment()
  experiment.start()

