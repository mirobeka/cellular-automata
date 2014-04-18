from pybrain.optimization import CMAES
from numpy import array
import logging

def learn(obj_fun, inital_weights):
    l = CMAES(obj_fun, inital_weights, minimize=True, verbose=True)
    res = l.learn()
    log = logging.getLogger("CMAES")
    log.debug("result is: {}".format(res))
    return res[0]

