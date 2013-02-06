from cellular_automata.rules.base import Rule
import numpy as np
import pyopencl as cl

class RuleCL(Rule):
  '''This is just wrapper to equip base Rule class with some
  open cl helper methods.
  '''
  pass

class MLPRule(RuleCL):
  @staticmethod
  def get_kernel(c_decl):
    fstr = ""
    with open("kernels/mlp.cl","r") as f:
      fstr = "".join(f.readlines())
    fstr = c_decl + fstr
    print(fstr)
    return fstr
