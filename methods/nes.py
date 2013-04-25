from numpy import array
from pybrain.optimization import ExactNES

def learn(obj_fun, init_values):
    l = ExactNES(obj_fun, init_values, minimize=True, verbose=True)
    res = l.learn()
    return res[0]
