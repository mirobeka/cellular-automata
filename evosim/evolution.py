from __future__ import print_function
from utils.loader import module_loader
import numpy as np
import logging
import time
import sys
import os

ca_directory = os.getcwd()
if ca_directory not in sys.path:
    sys.path.insert(0, ca_directory)


class Embryo(object):
    """Embryo
    """

    def __init__(self, cfg, save_to):
        self.conf = module_loader(cfg)
        self.save_to = save_to

        objective_class = self.conf["evolution"]["objective"]
        pattern_file = self.conf["evolution"]["pattern"]

        self.objective = objective_class(cfg, pattern_file)
        self.objective.callback = self.save_result
        self.strategy = self.conf["evolution"]["strategy"]

    def get_initial_weights(self):
        # for now, return just initial weights from configuration file
        values = eval(self.conf["evolution"]["initial_weights"])
        return np.array(values)

    def evolve(self):
        initial_weights = self.get_initial_weights()
        self.objective.best_weights = initial_weights
        self.result = self.strategy.learn(self.objective, initial_weights)

    def get_result(self):
        result = {}
        result["error"] = self.objective.min_error
        result["weights"] = self.objective.best_weights
        result["pattern"] = self.objective.pattern_file
        result["generations"] = self.objective.generation
        result["lattice_age"] = self.objective.lattice_age
        result["average_lattice_age"] = np.mean(self.objective.lattice_age_list)
        result["progress"] = self.objective.progress

        return result

    def save_result(self):
        result = self.get_result()
        with open(self.save_to, "w") as fp:
            fp.write(str(result["error"])+"\n")
            fp.write("["+ ",".join(map(str,result["weights"])) +"]\n")
            fp.write(str(result["pattern"])+"\n")
            fp.write(str(result["generations"])+"\n")
            fp.write(str(result["lattice_age"])+"\n")
            fp.write(str(result["average_lattice_age"])+"\n")
            fp.write("\n")
            fp.write("progress:\n")
            for (generation, error, weights) in result["progress"]:
                fp.write(str(generation) + " " + str(error)+":")
                fp.write("["+ ",".join(map(str,result["weights"])) +"]\n")

def evolve_weights(cfg, save_to):
    """Creates embryo, lets it evolve

    :param cfg: path to project configuration file
    :returns: list of evolved weights
    """
    embryo = Embryo(cfg, save_to)
    try:
        embryo.evolve()
    except KeyboardInterrupt:
        # take the best weights and save them
        log = logging.getLogger("MAIN")
        log.exception("Terminating evolution")

    try:
        embryo.save_result()
    except:
        log.exception("Exception while saving results")
        log.info(embryo.get_result())

