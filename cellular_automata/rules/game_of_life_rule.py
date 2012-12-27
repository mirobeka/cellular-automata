from cellular_automata.rules.base import Rule

class GameOfLifeRule(Rule):
  def getNextState(self, cell, neighbors):
    stateVector = self.getStateVector(cell, neighbors)
    return self.calculateState(stateVector)

  def getStateVector(self, cell, neighbors):
    stateVector = [cell.getState()]
    stateVector += [neigh.getState() for neigh in neighbors if neigh]
    return stateVector

  def calculateState(self, stateVector):
    noOfNeighborsAlive = sum(stateVector[1:])
    if stateVector[0] == 1 and  2 <= noOfNeighborsAlive <= 3:
      return 1
    elif stateVector[0]== 0 and noOfNeighborsAlive == 3:
      return 1
    else:
      return 0

