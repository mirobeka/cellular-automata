from cellular_automata.rules.base import Rule

from numpy import array
from pybrain.tools.shortcuts import buildNetwork

class MLPRule(Rule):
  def __init__(self, stateVectorLength = 5):
    Rule.__init__(self)
    self.stateVectorLength = stateVectorLength
    self.inputLayerLength = stateVectorLength*5
    self.net = buildNetwork(self.inputLayerLength, self.inputLayerLength*2, stateVectorLength)

  def updateNetworkWeights(self, weights):
    newWeights = array(weights)
    self.net._setParams(newWeights)

  def getWeights(self):
    return self.net.params

  def getNextState(self, cell, neighbors):
    # collect all data for neural network
    inVector = self.getInputVector(cell, neighbors)
    outVector = self.net.activate(inVector)
    return outVector

  def getInputVector(self, cell, neighbors):
    inVector = []
    inVector.extend(cell.getState())
    for neighs in neighbors.values():
      if len(neighs) == 0:
        inVector.extend([0]*self.stateVectorLength)
      else:
        inVector.extend([sum(x) for x in zip(*map(lambda cell: cell.getState(), neighs))])
    return inVector

  def initialState(self):
    return [0]*self.stateVectorLength

