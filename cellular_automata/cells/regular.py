from cellular_automata.cells.base import Cell

class SquareCell(Cell):
  def addNeighbors(self, neighbors):
    for direction, neigh in neighbors.items():
      self.neighs[direction].update(neigh)

  def set_neighbours(self, neighbours):
    self.neighs = neighbours

  def toDict(self):
    '''exports cells state, neighbours indices to dictionary (parsable by YAML)'''
    cell = {}
    cell["state"] = self.state
    cell["position"] = self.position
    cell["neighbours"] = [
        (direction, set(map(lambda neigh: neigh.position, directionNeighs)))
        for direction, directionNeighs in self.neighs.items()]
    return cell

class VariableSquareCell(SquareCell):
  def __init__(self):
    SquareCell.__init__(self)
    self.size = 1

  def wantsGrow(self):
    return self.state.wants_grow and not self.state.wants_divide

  def wantsDivide(self):
    return self.state.wants_divide and not self.state.wants_grow and self.size >= 4

  def grow(self):
    for direction in self.neighs.keys():
      if self.canMergeWithOthers(direction):
        return self.getCellsToMerge(direction)

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

  def toDict(self):
    pass

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

