from cellular_automata.rules.base import Rule

from numpy import array
from pybrain.tools.shortcuts import buildNetwork

class MLPRule(Rule):
  def __init__(self, stateVectorLength = 5):
    Rule.__init__(self)
    self.stateVectorLength = stateVectorLength
    self.inputLayerLength = stateVectorLength*5
    self.net = buildNetwork(self.inputLayerLength, self.inputLayerLength, stateVectorLength)

  def getWeights(self):
    return self.net.params

  def set_weights(self, weights):
    newWeights = array(weights)
    self.net._setParameters(newWeights)
    print("set weights to = " + str(self.net.params))

  def get_next_state(self, cell, neighbors):
    # collect all data for neural network
    inVector = self.getInputVector(cell, neighbors)
    outVector = self.net.activate(inVector)
    return outVector

  def getInputVector(self, cell, neighbors):
    inVector = []
    inVector.extend(cell.state.rgb)
    for neighs in neighbors.values():
      if len(neighs) == 0:
        inVector.extend([0]*self.stateVectorLength)
      else:
        inVector.extend([sum(x) for x in zip(*map(lambda cell: cell.state.rgb, neighs))])
    return inVector

