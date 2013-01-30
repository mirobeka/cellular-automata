from cellular_automata.cells.base import Cell

class SquareCell(Cell):
  def __init__(self):
    Cell.__init__(self)
    self.initializeState()

  def initializeState(self):
    self.state = [0,0,0]
  
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
    self.initializeState()

  def initializeState(self):
    initialCellState = [0,0,0,0,0]
    self.state = initialCellState

  def wantsGrow(self):
    return self.state[-2] > 0 and not self.state[-1] < 0

  def wantsDivide(self):
    return self.state[-2] < 0 and self.state[-1] > 0 and self.size >= 4

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

