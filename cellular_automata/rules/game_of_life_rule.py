from cellular_automata.rules.base import Rule

class GameOfLifeRule(Rule):
  def getNextState(self, cell, neighs):
    stateVector = self.getStateVector(cell, neighs)
    return self.calculateState(stateVector)

  def getStateVector(self, cell, neighs):
    stateVector = [cell.getState()]
    stateVector += self.getNeighsStates(neighs)
    return stateVector

  def getNeighsStates(self, neighs):
    listOfStates = []
    for direction, neigh in neighs.items():
      if len(neigh) > 0:
        neighItem = iter(neigh).next()
        listOfStates.append(neighItem.getState())
    return listOfStates

  def calculateState(self, stateVector):
    noOfNeighborsAlive = sum(stateVector[1:])
    if stateVector[0] == 1 and 2 <= noOfNeighborsAlive <= 3:
      return 1
    elif stateVector[0]== 0 and noOfNeighborsAlive == 3:
      return 1
    else:
      return 0

