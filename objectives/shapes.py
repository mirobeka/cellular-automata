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
            print("unstable configuration of lattice")
            return 99999.0
        else:
            error = self.error_function(self.desired_lattice, lattice)
            return error


class CircleObjective(Objective):
    """Objective that is trying to learn how to model circular shape"""
    pass    # TODO


class EnergyStopCriterion(object):
    """ Energy stop criterion is really important part of evolution. It drives
    evolution to a certain very different solutions. As an example, we could 
    take stopping criterion based on variance of lattice in some time window.
    In our case, we used window of 16 energy variances from mean energy and sum
    those up. If variance is low, we consider this as stable state and forther
    iterations are stopped.

    Now in this kind of stopping criterion, is high posibility, that semi stable
    configuration will emerge. Because we measure global variance of all cells,
    regular cyclic changes seems as stable to variance evaluation, but in reallity
    solution is semi stable. That means, there is some pattern that is repeating
    over and over again and doesn't do exactly what we wanted to evolve.

    This is really good example, how such a simple part as when we consider lattice
    as stable, could drive evolution to periodic solutions instead of perfectly
    stable one.

    The regularity of repeating pattern also depends on main goal, but also from
    time window that we measure variance in. In shorter time windows, solution
    that emerges are more likely similiar to semafor behaviour and blinking.
    However, stretching time window to at least 16 time steps, enables evolution
    to create more smooth transition resembling waves traveling in one direction.

    Very interesting way, is also stretch time window even more, and check variance
    over the whole time span of iteration of CA. This particullar setting returns

    """
    def __init__(self):
        self.energy_threshold = 0.01
        self.max_time = 1024

    def should_run(self, lattice):
        if lattice.time >= self.max_time:
            lattice.chaotic = True
            return False
        elif lattice.energy_variance(lattice.time) < self.energy_threshold:
            return False
        else:
            return True
