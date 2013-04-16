from cellular_automata.creator import create_automaton
from cellular_automata.creator import load_automaton


class Objective(object):
    """This is just abstract class to be extended. Extend this class for your
    objective that should be optimized.
    """

    def error_function(self, pattern, lattice):
        """ error funtion compare given latice with desired pattern and returns
        scalar value describing difference between those 2 lattices

        This method should be implemented to reflect objective that should be
        optimized.

        For example, if I want to optimized structure and topology of cellular
        automata(CA), in this function should be compared resulting lattice
        and  defined pattern and thid comparison reflected by scalar value.

        In other case, I we want to optimise structure and also states of CA
         se should compare states and structure and then sum this error and
         return scalar value
        """
        raise NotImplementedError("error function not implemented")

    def objective_function(self, vector):
        """ Objective funtion is main function that is minimized by cma-es
        algorithm. In our case, we are optimizing weights of neural network,
        but we can optimize anything we want.

        On the input of objective_function is optimized vector of values. On
        the output of objective_function must be scalar value that is minimized.


        This method should be implemented in a way that suits your
        optimalization needs.
        """
        raise NotImplementedError("method objective_function not implemented")


class TwoBandObjective(Objective):
    def __init__(self, lattice_file):
        Objective.__init__(self)
        self.lattice_file = lattice_file
        self.initialize_experiment_parameters()

    def initialize_experiment_parameters(self):
        self.desired_lattice = load_automaton(self.lattice_file)
        self.dimensions = (self.desired_lattice.width,
                           self.desired_lattice.height)
        self.resolution = self.desired_lattice.resolution
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
        self.energy_threshold = 10 ** -5
        self.max_time = 1024

    def should_run(self, lattice):
        if lattice.time >= self.max_time:
            lattice.chaotic = True
        print("energy variance: {}".format(lattice.energy_variance(16)))
        return lattice.time < self.max_time and lattice.energy_variance(
            16) > self.energy_threshold
