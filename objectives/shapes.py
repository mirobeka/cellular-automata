from objectives.base import Objective
from cellular_automata.creator import create_automaton
from cellular_automata.creator import load_automaton


class TwoBandObjective(Objective):
    def __init__(self, lattice_file):
        self.initialize_experiment_parameters(lattice_file)

    @classmethod
    def create_new_objective(cls, conf_file, desired_pattern):
        objective = cls(desired_pattern)
        objective.conf_file = conf_file
        return objective

    def initialize_experiment_parameters(self, desired_pattern):
        # load desired automaton from serialized file
        self.desired_lattice = load_automaton(desired_pattern)

        # load all important properties
        self.dimensions = (self.desired_lattice.width,
                           self.desired_lattice.height)
        self.resolution = self.desired_lattice.resolution

        # create energy stop criterion. This way is good for now,
        # later we could be more flexible about choosing stop criterion
        self.stop_criterion = EnergyStopCriterion()
        self.max_difference = self.get_max_difference(self.desired_lattice)

    @staticmethod
    def get_max_difference(desired_lattice):
        """Return maximum possible difference of current lattice from desired
         lattice. Also if we go over MAXINT, python automatically converts to
         long

        :param desired_lattice: desired lattice which we want to fit
        :return: maximum possible difference between current and desired lattice
        """
        max_difference = len(desired_lattice.cells) * 65536
        return max_difference

    def error_function(self, desired, lattice):
        """check desired pattern with given lattice. Return sum of state
        differences
        """
        difference = .0
        for key in desired.cells.keys():
            difference += (desired.cells[key].state.grayscale - lattice.cells[
                key].state.grayscale) ** 2

        # normalize difference
        normalized_difference = difference / self.max_difference
        return normalized_difference

    def objective_function(self, weights):
        """Constructs cellular automata, set weights of MLP as rule for cellular
        automata, run cellular automata until it stops and compare result with
        desired pattern. In this case desired pattern is two band.
        """
        lattice = create_automaton(self.conf_file)
        lattice.rule.set_weights(weights)
        lattice.run(self.stop_criterion)
        if lattice.chaotic:   # if lattice doesn't have stable configuration
            print("Lattice is chaotic. Return fitness 1.0")
            return 1.0
        return self.error_function(self.desired_lattice, lattice)


class CircleObjective(Objective):
    """Objective that is trying to learn how to model circular shape
    """
    pass    # TODO


class EnergyStopCriterion(object):
    def __init__(self):
        self.energy_threshold = 10 ** -3
        self.max_time = 1024

    def should_run(self, lattice):
        if lattice.time >= self.max_time:
            lattice.chaotic = True
        return lattice.time < self.max_time and lattice.energy_variance(
            16) > self.energy_threshold
