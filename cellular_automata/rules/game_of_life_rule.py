from cellular_automata.rules.base import Rule

class GameOfLifeRule(Rule):
  def get_next_state(self, cell, neighs):
    state_vector = self.get_state_vector(cell, neighs)
    return self.calculate_state(cell.state, state_vector)

  def get_state_vector(self, cell, neighs):
    state_vector = [cell.state.alive]
    state_vector += self.get_neighs_states(neighs)
    return state_vector

  def get_neighs_states(self, neighs):
    list_of_states = []
    for direction, neigh in neighs.items():
      if len(neigh) > 0:
        neigh_item = iter(neigh).next()
        list_of_states.append(neigh_item.state.alive)
    return list_of_states

  def calculate_state(self, state, state_vector):
    new_state = state.create_state()
    no_of_neighbors_alive = sum(state_vector[1:])
    if state_vector[0] and 2 <= no_of_neighbors_alive <= 3:
      new_state.alive = True
    elif state_vector[0] and no_of_neighbors_alive == 3:
      new_state.alive = True
    else:
      new_state.alive = False
    return new_state

