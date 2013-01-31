import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

import cmaes.cma as cma
from cmaes.objectives import TwoBandObjective
from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
import yaml

class CmaesExperiment:
  def __init__(self):
    self.objective = TwoBandObjective()

  def evolve(self):
    initial_weights = self.get_initial_values()
    result = cma.fmin(
        self.objective.objective_function,
        initial_weights,
        0.3,
        verb_disp=0)
    self.save_result_to_file(result)
    
  def save_result_to_file(self, result):
    data = "empty"
    try:
      data = yaml.dump(result)
    except:
      print("error")

    print(result)

    with open("data/result.yaml", 'w+') as f:
      f.write(data)

  def get_initial_values(self):
    return [0.0]*288

if __name__ == "__main__":
  experiment = CmaesExperiment()
  experiment.evolve()

