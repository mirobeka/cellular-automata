import sys
import os
from ConfigParser import ConfigParser
from utils.loader import get_conf

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
        except Exception as e:
            print("Exception while evolving weights", e)
        evo.save_results("data/results")

    def initialize_new_evolution(self, conf_file):
        self.conf = get_conf(conf_file)

        objective_class = self.conf["evolution"]["objective"]
        lattice_file = self.conf["evolution"]["desired_pattern"]
        self.objective = objective_class.create_new_objective(lattice_file)

        strategy_class = self.conf["evolution"]["strategy"]
        self.strategy = strategy_class()

    def evolve(self):
        # there should be some kind of clever way of dealing with different
        # optimization methods, but for new, we use only CMAES
        initial_values = self.get_initial_values()
        self.result = self.strategy.fmin(self.objective.objective_function, initial_values, verb_time=100)

    def get_initial_values(self):
        # how many weights?
        rule_class = self.conf["simulation"]["rule"]
        rule = rule_class()
        return rule.total_number_of_weights()

    def save_results(self, file_name="data/result"):
        try:
            with open(file_name, "w") as results_file:
                results_file.write(str(self.result))
        except IOError as e:
            print("failed to write results to file")
            print(e)
            print("weights are : {}".format(self.result))
        print("weight successfully saved to {}".format(file_name))
