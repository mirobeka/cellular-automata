from objectives.base import Objective
from cellular_automata.creator import create_automaton
from cellular_automata.creator import load_automaton
from cellular_automata.creator import load_pattern
from utils.loader import module_loader
import logging

log = logging.getLogger("OBJECTIVE")


class PatternObjective(Objective):
    def __init__(self, conf_file, pattern_file):
        self.conf_file = conf_file
        self.pattern_file = pattern_file
        self.loaded_modules = module_loader(conf_file)

        # load desired automaton from serialized file
        self.pattern = load_pattern(pattern_file)

        # load all important properties
        self.dimensions = (self.pattern.width,
                           self.pattern.height)
        self.resolution = self.pattern.resolution

        stop_crit = self.loaded_modules["stopcriterion"]["criterion"]
        stop_crit_args = dict([(arg, val) for arg,val in self.loaded_modules["stopcriterion"].items() if arg != "criterion"])

        self.stop_criterion = stop_crit(**stop_crit_args)
        self.max_difference = self.get_max_difference(self.pattern)

        self.min_error = 1.0
        self.best_weights = None
        self.lattice_age = 0
        self.lattice_age_list = []
        self.progress = []
        self.generation = 0

        self.callback = None

    @staticmethod
    def get_max_difference(pattern):
        """Max error value"""
        max_difference = len(pattern.cells) * 65536
        return max_difference

    def generation_callback(self, cmaes_object):
        self.generation = cmaes_object.numLearningSteps

    def error_function(self, pattern, lattice):
        """check desired pattern with given lattice. Return sum of state
        differences

        TODO: we should be able to select which property of state to compare
        """
        difference = .0
        for key in pattern.cells.keys():
            difference += (pattern.cells[key] - lattice.cells[
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

        self.lattice_age_list.append(lattice.age)

        log.info("iterations {}".format(lattice.age))

        if lattice.chaotic:   # if lattice doesn't have stable configuration
            log.info("unstable lattice")
            return 1.0
        else:
            error = self.error_function(self.pattern, lattice)
            if error < self.min_error:
                log.info("updating minimal error to: {}".format(error))
                self.min_error = error
                self.best_weights = weights
                self.lattice_age = lattice.age
                self.progress.append((self.generation,error,weights))

                if self.callback is not None:
                    self.callback()
            log.debug("error: {}".format(error))
            return error

class StopCriterion(object):
    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

class AgeCriterion(StopCriterion):
    def should_run(self, lattice):
        return lattice.age < self.max_age


class EnergyCriterion(StopCriterion):
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
    over the whole time span of iteration of CA.

    """
    def __init__(self, **kw):
        super(EnergyCriterion, self).__init__(**kw)
        self.energy_threshold = 0.01
        self.energy_difference_threshold = 0.0001
        self.max_age = 1024

    def should_run(self, lattice):
        # print("lattice energy difference:{}".format(lattice.energy_difference()))
        if lattice.age >= self.max_age:
            lattice.chaotic = True
            return False
        # elif lattice.energy_variance() <= self.energy_threshold:
        elif lattice.energy_difference() <= self.energy_difference_threshold:
            return False
        else:
            return True
