from cellular_automata.cells.base import Cell

class SquareCell(Cell):
  def __init__(self, rule):
    Cell.__init__(self, rule)
    self.createEmptyNeighborhood()
    self.initializeState()

  def initializeState(self):
    self.setState(0)
  
  def createEmptyNeighborhood(self):
    self.neighs = {}
    directions = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
    for direction in directions:
      self.neighs[direction] = []

  def addNeighbors(self,neighbors):
    for direction, neigh in neighbors.items():
      if type(neigh) is list:
        self.neighs[direction] += neigh
      else:
        self.neighs[direction].append(neigh)

  def __str__(self):
    if self.getState():
      return "|*"
    else:
      return "|_"

class VariableSquareCell(SquareCell):
  def __init__(self, rule):
    SquareCell.__init__(self, rule)
    self.size = 1

  def initializeState(self):
    initialCellState = [0,0]
    self.setState(initialCellState)

  def joinCell(self, cell):
    # join with other cell
    pass

  def tearCell(sefl, cell):
    # tear join with cell
    pass

