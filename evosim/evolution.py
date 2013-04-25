import sys
import os
import time
from utils.loader import get_conf
import numpy as np

ca_directory = os.getcwd()
if ca_directory not in sys.path:
    sys.path.insert(0, ca_directory)


class Evolution(object):
    def __init__(self):
        pass

    @classmethod
    def new_evolution(cls, conf_file):
        """Creates new evolution where we try to evolve weights to neural
        network.

        :param conf_file: properties of evolution
        """
        evo = cls()
        evo.initialize_new_evolution(conf_file)
        try:
            evo.evolve()
        except:
            # take the best weights and save them
            evo.result = evo.objective.best_weights
            evo.save_results("data/results_{}".format(time.ctime().replace(" ","_")))
        else:
            evo.save_results("data/results_{}".format(time.ctime().replace(" ","_")))

    def initialize_new_evolution(self, conf_file):
        self.conf = get_conf(conf_file)

        objective_class = self.conf["evolution"]["objective"]
        desired_pattern = self.conf["evolution"]["desired_pattern"]
        self.objective = objective_class.create_new_objective(
            conf_file, desired_pattern)

        self.strategy = self.conf["evolution"]["strategy"]

    def evolve(self):
        # there should be some kind of clever way of dealing with different
        # optimization methods, but for new, we use only CMAES
        initial_values = self.get_initial_values()
        self.objective.best_weights = initial_values
        self.result = self.strategy.learn(self.objective.objective_function, initial_values)

    def get_initial_values(self):
        if self.conf["evolution"]["initial_weights"] is None:
            # how many weights?
            rule_class = self.conf["simulation"]["rule"]
            rule = rule_class()
            values = [0]*rule.total_number_of_weights()
        else:
            values = eval(self.conf["evolution"]["initial_weights"])

        return np.array(values)

    def save_results(self, file_name="data/result"):
        try:
            with open(file_name, "w") as results_file:
                results_file.write(str(self.result))
        except IOError as e:
            print("failed to write results to file")
            print(e)
            print("weights are : {}".format(self.result))
        print("weight successfully saved to {}".format(file_name))
