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

  def addNeighbors(self, neighbors):
    for direction, neigh in neighbors.items():
      if type(neigh) is list:
        self.neighs[direction] += filter(lambda x: x, neigh)
      elif neigh:
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
    self.directions = ["north", "east", "south", "west"]

  def initializeState(self):
    initialCellState = [0,0]
    self.setState(initialCellState)

  def wantsGrow(self):
    return self.getState()[1]

  def grow(self):
    for direction, neigh in self.neighs.items():
      if self.mergeConstraints(direction, neigh):
        cellsToMerge = neigh[0].getCellsToMerge([self], direction)
        return self.mergeCells(cellsToMerge)

  def mergeCells(self, cellsToMerge):
    newCell = VariableSquareCell(self.rule)
    newCell.size = 4*self.size
    for direction in self.directions:
      newCell.neighs[direction] = [neigh for cell in cellsToMerge for neigh in cell.neighs[direction] if neigh not in cellsToMerge]
    
    for direction, neighs in newCell.neighs.items():
      map(lambda neigh: neigh.updateNeighConnection(direction, [newCell], cellsToMerge), neighs)
    return cellsToMerge, [newCell]

  def updateNeighConnection(self, direction, cellsToAdd, cellsToRemove):
    oppositeDirection = self.reverseDirection(direction)
    for oldNeigh in cellsToRemove:
      if oldNeigh in self.neighs[oppositeDirection]:
        self.neighs[oppositeDirection].remove(oldNeigh)
    self.neighs[oppositeDirection] += cellsToAdd

  def mergeConstraints(self, direction, neigh, startCell = None):
    startCell = self if not startCell else startCell
    return len(neigh) == 1 and self.sameSize(neigh[0]) and neigh[0].canMergeWithOthers(startCell, direction)

  def sameSize(self, otherCell):
    return self.size == otherCell.size

  def getCellsToMerge(self, cells, direction):
    if cells[0] == self:
      return cells
    else:
      newDirection = self.turnRight(direction)
      neigh = self.neighs[newDirection][0]
      return neigh.getCellsToMerge(cells+[self], newDirection)

  def canMergeWithOthers(self, startCell, direction):
    if startCell == self:
      return True
    else:
      newDirection = self.turnRight(direction)
      return self.mergeConstraints(newDirection, self.neighs[newDirection], startCell)

  def turnRight(self, direction):
    if direction == "north":
      return "east"
    elif direction == "east":
      return "south"
    elif direction == "south":
      return "west"
    elif direction == "west":
      return "north"
    else:
      raise Exception( direction + " is wrong direction to turn right!")

  def reverseDirection(self, direction):
    if direction == "north":
      return "south"
    elif direction == "east":
      return "west"
    elif direction == "south":
      return "north"
    elif direction == "west":
      return "east"
    else:
      raise Exception(direction + " is wrong direction to reverse!")

