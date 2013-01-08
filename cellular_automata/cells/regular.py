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
      self.neighs[direction] = set()

  def addNeighbors(self, neighbors):
    for direction, neigh in neighbors.items():
      self.neighs[direction].update(neigh)

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
    self.initializeState()
    self.removeUnusedNeighsDirections()

  def removeUnusedNeighsDirections(self):
    for direction in self.neighs.keys():
      if direction not in self.directions:
        del self.neighs[direction]

  def initializeState(self):
    initialCellState = self.rule.initialState()
    self.setState(initialCellState)

  def wantsGrow(self):
    return self.getState()[-2] > 0.5 and not self.getState()[-1] <= 0.5

  def wantsDivide(self):
    return not self.getState()[-2] > 0.5 and self.getState()[-1] <= 0.5 and self.size >= 4

  def divide(self):
    # create 4 new cells
    cellNW = VariableSquareCell(self.rule)
    cellNE = VariableSquareCell(self.rule)
    cellSW = VariableSquareCell(self.rule)
    cellSE = VariableSquareCell(self.rule)

    cellNW.size = self.size/4
    cellNE.size = self.size/4
    cellSW.size = self.size/4
    cellSE.size = self.size/4

    # position
    halfRadius = self.radius/2

    cellNW.x = self.x - halfRadius
    cellNW.y = self.y - halfRadius
    cellNW.radius = halfRadius
    cellNE.x = self.x + halfRadius
    cellNE.y = self.y - halfRadius
    cellNE.radius = halfRadius
    cellSW.x = self.x - halfRadius
    cellSW.y = self.y + halfRadius
    cellSW.radius = halfRadius
    cellSE.x = self.x + halfRadius
    cellSE.y = self.y + halfRadius
    cellSE.radius = halfRadius

    # create neighbor connections
    cellNW.neighs["south"].add(cellSW)
    cellNW.neighs["east"].add(cellNE)
    cellNE.neighs["south"].add(cellSE)
    cellNE.neighs["west"].add(cellNW)
    cellSW.neighs["north"].add(cellNW)
    cellSW.neighs["east"].add(cellSE)
    cellSE.neighs["north"].add(cellNE)
    cellSE.neighs["west"].add(cellSW)

    newCells = {}
    newCells["north"] = [cellNW, cellNE]
    newCells["east"] = [cellNE, cellSE]
    newCells["south"] = [cellSE, cellSW]
    newCells["west"] = [cellNW, cellSW]

    for direction in self.directions:
      directionNeighbors = self.neighs[direction]
      for directionNeighbor in directionNeighbors:
        for newCell in newCells[direction]:
          if directionNeighbor.isNeighborWith(newCell):
            newCell.neighs[direction].add(directionNeighbor)

    # now we have new cells with correct neighs.
    # this time we have to update rest of the neighborhood
    for newCell in [cellNW, cellNE, cellSW, cellSE]:
      self.updateNeighborhood(newCell, [self])

    return [self], [cellNW, cellNE, cellSW, cellSE]

  def isNeighborWith(self, cell):
    selfLeft = self.x - self.radius
    selfRight = self.x + self.radius
    cellLeft = cell.x - cell.radius
    cellRight = cell.x + cell.radius

    selfTop = self.y - self.radius
    selfBottom = self.y + self.radius
    cellTop = cell.y - cell.radius
    cellBottom = cell.y + cell.radius

    if selfRight < cellLeft or cellRight < selfLeft:
      return False
    elif selfBottom < cellTop or cellBottom < selfTop:
      return False
    return True

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
      newCell.neighs[direction] = set([neigh for cell in cellsToMerge for neigh in cell.neighs[direction] if neigh not in cellsToMerge])

  def updateNeighborhood(self, newCell, oldCells):
    for direction, neighs in newCell.neighs.items():
      for neigh in neighs:
        neigh.removeOldNeighbors(direction, oldCells)
        neigh.addNewNeighbors(direction, [newCell])

  def removeOldNeighbors(self, direction, cellsToRemove):
    oppositeDirection = self.reverseDirection(direction)
    for oldNeigh in cellsToRemove:
      if oldNeigh in self.neighs[oppositeDirection]:
        self.neighs[oppositeDirection].remove(oldNeigh)

  def addNewNeighbors(self, direction, cellsToAdd):
    oppositeDirection = self.reverseDirection(direction)
    self.neighs[oppositeDirection].update(cellsToAdd)

  def getCellsToMerge(self, direction):
    return self._getCellsToMerge([], direction)

  def _getCellsToMerge(self, cells, direction):
    if len(cells) is 4:
      return cells
    else:
      newDirection = self.turnRight(direction)
      neigh = iter(self.neighs[direction]).next()
      return neigh._getCellsToMerge(cells+[self], newDirection)

  def mergeConstraints(self, direction):
    ''' cell can merge with other when they are same size and cell are aligned.'''
    neigh = self.neighs[direction]
    if len(neigh) == 1:
      neighItem = iter(neigh).next()
      return self.sameSize(neighItem) and neighItem.wantsGrow()
    return False

  def canMergeWithOthers(self, direction):
    return self._canMergeWithOthers(4, direction)

  def _canMergeWithOthers(self, cellCountdown, direction):
    if cellCountdown is 0:
      return True
    else:
      if self.mergeConstraints(direction):
        newDirection = self.turnRight(direction)
        neighItem = iter(self.neighs[direction]).next()
        return neighItem._canMergeWithOthers(cellCountdown-1, newDirection)
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

