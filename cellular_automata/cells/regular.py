from cellular_automata.cells.base import Cell
from cellular_automata.cells.base import CellCL

class SquareCellCL(CellCL):
  def add_neighbors(self, neighbors):
    for direction, neigh in neighbors.items():
      self.neighs[direction].update(neigh)
    # TODO: adjust indices

  def set_neighbours(self, neighbours):
    self.neighs = neighbours

  def set_neighbours_indices(self, neighs_indices):
    # in cell data first 8 values are indices to neighbours in clockwise order
    # n,ne,e,se,s,sw,w,nw
    for i,index in enumerate(neighs_indices):
      self.data[i] = index

  def to_dict(self):
    # TODO
    pass

class SquareCell(Cell):
  def add_neighbors(self, neighbors):
    for direction, neigh in neighbors.items():
      self.neighs[direction].update(neigh)

  def set_neighbours(self, neighbours):
    self.neighs = neighbours

  def to_dict(self):
    '''exports cells state, neighbours indices to dictionary (parsable by YAML)'''
    cell = {}
    cell["state"] = self.state
    cell["position"] = self.position
    cell["neighbours"] = [
        (direction, set(map(lambda neigh: neigh.top_left_corner, direction_neighs)))
        for direction, direction_neighs in self.neighs.items()]
    return cell

class VariableSquareCell(SquareCell):
  def __init__(self):
    SquareCell.__init__(self)
    self.size = 1

  def wants_grow(self):
    return self.state.wants_grow and not self.state.wants_divide

  def wants_divide(self):
    return self.state.wants_divide and not self.state.wants_grow and self.size >= 4

  def grow(self):
    for direction in self.neighs.keys():
      if self.can_merge_with_others(direction):
        return self.get_cells_to_merge(direction)

  def get_cells_to_merge(self, direction):
    return self._get_cells_to_merge([], direction)

  def _get_cells_to_merge(self, cells, direction):
    if len(cells) is 4:
      return cells
    else:
      new_direction = self.turn_right(direction)
      neigh = iter(self.neighs[direction]).next()
      return neigh._get_cells_to_merge(cells+[self], new_direction)

  def merge_constraints(self, direction):
    ''' cell can merge with other when they are same size and cell are aligned.'''
    neigh = self.neighs[direction]
    if len(neigh) == 1:
      neigh_item = iter(neigh).next()
      return self.same_size(neigh_item) and neigh_item.wants_grow()
    return False

  def can_merge_with_others(self, direction):
    return self._can_merge_with_others(4, direction)

  def _can_merge_with_others(self, cell_countdown, direction):
    if cell_countdown is 0:
      return True
    else:
      if self.merge_constraints(direction):
        new_direction = self.turn_right(direction)
        neigh_item = iter(self.neighs[direction]).next()
        return neigh_item._can_merge_with_others(cell_countdown-1, new_direction)
      else:
        return False

  def to_dict(self):
    pass

  def same_size(self, other_cell):
    return self.size == other_cell.size

  def turn_right(self, direction):
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

  def reverse_direction(self, direction):
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

