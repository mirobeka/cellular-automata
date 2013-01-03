from cellular_automata.cells.base import Cell

class SquareCell(Cell):
  def __init__(self, rule):
    Cell.__init__(self, rule)
    self.createEmptyNeighborhood()
    self.initializeState()
    self.setPosition((0,0))
    self.radius = 8

  def setPosition(self, (x,y)):
    self.x = x
    self.y = y

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
    initialCellState = self.rule.initialState()
    self.setState(initialCellState)

  def wantsGrow(self):
    return self.getState()[3]

  def grow(self):
    for direction in self.directions:
      if self.canMergeWithOthers(direction):
        cellsToMerge = self.getCellsToMerge(direction)
        return self.mergeCells(cellsToMerge)

  def mergeCells(self, cellsToMerge):
    newCell = self.createNewCell(cellsToMerge)
    self.putNewCellIntoNeighborhood(newCell, cellsToMerge)
    return cellsToMerge, [newCell]

  def createNewCell(self, cellsToMerge):
    newCell = VariableSquareCell(self.rule)
    newCell.size = len(cellsToMerge)*self.size
    newCell.setPosition(self.interpolateCenter(cellsToMerge))
    newCell.radius = self.radius * 2
    return newCell

  def putNewCellIntoNeighborhood(self, newCell, cellsToMerge):
    self.setNeighborsOfNewCell(newCell, cellsToMerge)
    self.updateNeighborhood(newCell, cellsToMerge)

  def setNeighborsOfNewCell(self, newCell, cellsToMerge):
    for direction in self.directions:
      newCell.neighs[direction] = [neigh for cell in cellsToMerge for neigh in cell.neighs[direction] if neigh not in cellsToMerge]

  def updateNeighborhood(self, newCell, cellsToMerge):
    for direction, neighs in newCell.neighs.items():
      for neigh in neighs:
        neigh.removeOldNeighbors(direction, cellsToMerge)
        neigh.addNewNeighbors(direction, [newCell])

  def removeOldNeighbors(self, direction, cellsToRemove):
    oppositeDirection = self.reverseDirection(direction)
    for oldNeigh in cellsToRemove:
      if oldNeigh in self.neighs[oppositeDirection]:
        self.neighs[oppositeDirection].remove(oldNeigh)

  def addNewNeighbors(self, direction, cellsToAdd):
    oppositeDirection = self.reverseDirection(direction)
    self.neighs[oppositeDirection] += cellsToAdd

  def getCellsToMerge(self, direction):
    return self._getCellsToMerge([], direction)

  def _getCellsToMerge(self, cells, direction):
    if len(cells) is 4:
      return cells
    else:
      newDirection = self.turnRight(direction)
      neigh = self.neighs[direction][0]
      return neigh._getCellsToMerge(cells+[self], newDirection)

  def mergeConstraints(self, direction):
    ''' cell can merge with other when they are same size and cell are aligned.'''
    neigh = self.neighs[direction]
    return len(neigh) == 1 and self.sameSize(neigh[0]) and neigh[0].wantsGrow()

  def canMergeWithOthers(self, direction):
    return self._canMergeWithOthers(4, direction)

  def _canMergeWithOthers(self, cellCountdown, direction):
    if cellCountdown is 0:
      return True
    else:
      if self.mergeConstraints(direction):
        newDirection = self.turnRight(direction)
        return self.neighs[direction][0]._canMergeWithOthers(cellCountdown-1, newDirection)
      else:
        return False

  def interpolateCenter(self, cells):
    one = cells[0]
    opposite = cells[2]
    x = (one.x + opposite.x) / 2
    y = (one.y + opposite.y) / 2
    return x,y

  def sameSize(self, otherCell):
    return self.size == otherCell.size

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

