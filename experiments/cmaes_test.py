import sys, os

ca_directory = os.getcwd()
if ca_directory not in sys.path:
    sys.path.insert(0, ca_directory)

# import cmaes.cma as cma
# import cmaes.barecmaes2 as barecma
from pybrain.optimization import CMAES
from cmaes.objectives import TwoBandObjective
from cellular_automata.lattices.equiangular import DiffusionSquareLattice
import numpy as np


class CmaesExperiment:
    def __init__(self):
        self.objective = TwoBandObjective()

    def evolve(self):
        initial_weights = self.get_initial_values()
        # result = cma.fmin(
        #     self.objective.objective_function,
        #     initial_weights,
        #     0.3,
        #     verb_disp=10)
        # self.save_result_to_file(result)

        # pybrain version
        optimizer = CMAES(self.objective.objective_function, initial_weights,
                          minimize=True, verbose=True)
        optimizer.learn()

    def save_result_to_file(self, result):
        data = "empty"
        try:
            data = str(result[4])
            data += "\n" + str(result[5])
            data += "\n" + str(result[6])
        except:
            print("error")

        print(result)

        with open("data/result", 'w+') as f:
            f.write(data)

    def get_initial_values(self):
        return np.random.rand(84)


if __name__ == "__main__":
    experiment = CmaesExperiment()
    experiment.evolve()

