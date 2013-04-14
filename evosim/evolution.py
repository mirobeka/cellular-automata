import sys
import os
from ConfigParser import ConfigParser

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
            print("Exception while evolving weights")
            print(e)

        evo.save_results()

    def initialize_new_evolution(self, conf_file):
        self.conf = self.parse_configuration(conf_file)
        objective_class = self.get_objective_class()
        lattice_file = self.get_lattice_file()
        self.objective_instance = objective_class(lattice_file)

    def get_objective_class(self):
        return self.conf["objective"]

    def get_lattice_file(self):
        return self.conf["lattice_file"]

    def evolve(self):
        # which strategy to use?
        # fire up strategy with some sensible defaults
        self.result = [1, 2, 3]  # result should be list of weights in right
        # order
        return self.result

    def parse_configuration(self, conf_file):
        parser = ConfigParser()
        parser.read(conf_file)
        conf = {"a": 1}
        # make some more transformations
        return conf

    def save_results(self, file_name="data/result"):
        try:
            with open(file_name, "w") as results_file:
                results_file.write(str(self.result))
        except IOError as e:
            print("failed to write results to file")
            print(e)
            print("weights are : {}".format(self.result))
        print("weight successfully saved to {}".format(file_name))


