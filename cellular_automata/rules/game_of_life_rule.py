from cellular_automata.rules.base import Rule

class GameOfLifeRule(Rule):
  def getNextState(self, cellState, neighborsStates):
    noOfNeighborsAlive = sum(neighborsStates)
    if cellState == 1 and  2 <= noOfNeighborsAlive <= 3:
      return 1
    elif cellState == 0 and noOfNeighborsAlive == 3:
      return 1
    else:
      return 0

