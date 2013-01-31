from cellular_automata.rules.base import Rule

class GameOfLifeRule(Rule):
  def get_next_state(self, cell, neighs):
    state_vector = self.getStateVector(cell, neighs)
    return self.calculate_state(cell.state, state_vector)

  def getStateVector(self, cell, neighs):
    stateVector = [cell.state.alive]
    stateVector += self.getNeighsStates(neighs)
    return stateVector

  def getNeighsStates(self, neighs):
    listOfStates = []
    for direction, neigh in neighs.items():
      if len(neigh) > 0:
        neighItem = iter(neigh).next()
        listOfStates.append(neighItem.state.alive)
    return listOfStates

  def calculate_state(self, state, stateVector):
    new_state = state.create_state()
    noOfNeighborsAlive = sum(stateVector[1:])
    if stateVector[0] and 2 <= noOfNeighborsAlive <= 3:
      new_state.alive = True
    elif stateVector[0] and noOfNeighborsAlive == 3:
      new_state.alive = True
    else:
      new_state.alive = False
    return new_state

