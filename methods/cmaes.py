from pybrain.optimization import CMAES
from numpy import array
import logging

log = logging.getLogger("CMAES")

def learn(objective, inital_weights):
    l = CMAES(objective.objective_function, inital_weights, minimize=True, verbose=True, )

    l.maxLearningSteps = 2
    l._callback = objective.generation_callback

    log.debug("starting cmaes evolution")
    res = l.learn()
    log.debug("result is: {}".format(res))
    return res[0]

