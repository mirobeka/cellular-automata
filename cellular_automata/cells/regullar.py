from cellular_automata.cells.base import Cell

class SquareCell(Cell):
  def __init__(self, x, y, rule):
    Cell.__init__(self, rule)
    self.x = x
    self.y = y
    self.neighs = []
    self.state["current"] = 0
  
  def __str__(self):
    if self.getState():
      return "|*"
    else:
      return "|_"

  def addNeighbors(self, listOfNeighbors):
    for neigh in listOfNeighbors:
      self.neighs.append(neigh)

  def getCoordinates(self):
    return (self.x, self.y)

  def getNeighbors(self):
    return self.neighs

class VariableSquareCell(Cell):
  def __init__(self, rule):
    self.size = 1
    self.state = 0
    self.initializeNeighbors()

  def initializeNeighbors(self):
    self.neighs = {}
    self.neighs["north"] = [] 
    self.neighs["west"] = [] 
    self.neighs["east"] = [] 
    self.neighs["south"] = [] 

