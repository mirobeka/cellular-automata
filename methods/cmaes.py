from numpy import array
from pybrain.optimization import CMAES

def learn(obj_fun, init_values):
    l = CMAES(obj_fun, init_values, minimize=True, verbose=True)
    res = l.learn()
    return res[0]
