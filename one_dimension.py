import numpy
import pylab
import random
from array import array

class Rule:

  def __init__(self, rule):
    self.rule = rule
    # rule could be in following format
    # rule = {
    #   list of states : new state
    #   list of states : new state
    # }


  def getNextState(self, configuration):
    return self.rule[configuration]


class Cell:
  def __inti__(self, x, y):
    self.x = x
    self.y = y

    self.neighs = []
    # initialize neighbors

  def nextStep(self):
    # collect states of neighbors + cell state
    # call Rule.getNextState

class Lattice:
  def __init__(self, width, height):
    self.width = width
    self.height = height

    # lattice initialization
    self.lattice = [[Cell(cellX, cellY) for cellX in range(self.width)] for cellY in range(self.height)]

    # create connections between cells
    for y in range(self.height):
      for x in range(self.width):

  def nextTimeStep(self):
    # iterate over all cells and go to next state
    map(lambda row: map(lambda cell: cell.nextStep(), row),self.lattice)

class CellularAutomata:
  def __init__(self, maxSteps = 1000):
    self.lattice = Lattice(100,100)
    self.maxSteps = maxSteps

  def start(self):
    timeStep = 0
    while timeStep < self.timeStep:
      self.lattice.nextTimeStep()
      self.drawLattice()

  def drawLattice(self):
    # somehow draw lattice
    
  
