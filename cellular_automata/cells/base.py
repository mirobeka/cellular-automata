import numpy as np
import pyopencl as cl
import pyopencl.tools

class Cell(object):
  def __init__(self):
    self.rule = None
    self.age = 0
    self._position = (0,0)
    self._radius = 0
    self.initialize_state()

  @classmethod
  def create_initialized(cls, rule, neighbourhood, state_class):
    cell = cls()
    cell.rule = rule
    cell.neighs = neighbourhood.create_empty()
    cell.state = state_class.create_state()
    return cell

  @classmethod
  def create_empty(cls):
    return cls()

  def initialize_state(self):
    self._state = {}
    self._state[0] = None
    self._state[1] = None

  @property
  def radius(self):
    return self._radius

  @radius.setter
  def radius(self, radius):
    self._radius = radius
    self._tlc = (self.x-radius, self.y-radius)
    self._brc = (self.x+radius, self.y+radius)

  @property
  def state(self):
    return self._state[0]

  @state.setter
  def state(self, state):
    self._state[0] = state

  @property
  def next_state(self):
    return self._state[1]

  @next_state.setter
  def next_state(self, new_state):
    self._state[1] = new_state

  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, new_pos):
    if type(new_pos) == tuple and len(new_pos) == 2:
      self._position = new_pos
      self._tlc = tuple(x-self.radius for x in new_pos)
      self._brc = tuple(x+self.radius for x in new_pos)
    else:
      raise Exception("wrong position argument: {}".format(new_pos))

  def to_dict(self):
    raise NotImplementedError("method to_dict of cell is not implemented")

  @property
  def bounding_box(self):
    return self._tlc + self._brc

  @property
  def top_left_corner(self):
    return self._tlc

  @top_left_corner.setter
  def top_left_corner(self, new_pos):
    self.position = tuple(x+self.radius for x in new_pos)

  @property
  def bottom_right_corner(self):
    return self._brc

  @bottom_right_corner.setter
  def bottom_right_corner(self, new_pos):
    self.position = tuple(x-self.radius for x in new_pos)

  @property
  def x(self):
    return self._position[0]

  @x.setter
  def x(self, x):
    self._position = (x, self.y)

  @property
  def y(self):
    return self._position[1]

  @y.setter
  def y(self, y):
    self._position = (self.x, y)

  def compute_next_state(self):
    self.next_state = self.rule.get_next_state(self, self.neighs)

  def apply_next_state(self):
    self.state = self.next_state
    self.age += 1

  def get_neighbors(self):
    return self.neighs


class CellCL(Cell):
  '''This is base class for different cellular automata cells, but with
  open cl in mind.'''

  def __init__(self, data, index):
    self.data = data
    self.idx = index
    self.age = 0
    self._position = (0,0)
    self._radius = 0

  @classmethod
  def create_dtype_struct(cls, state_dtype):
    cell_dtype = [
      ("n",np.int), ("ne",np.int), ("e",np.int), ("se",np.int),
      ("s",np.int), ("sw",np.int), ("w",np.int), ("nw",np.int)
    ]
    np_dtype = np.dtype(cell_dtype + state_dtype)
    context = cl.create_some_context()
    dtype, c_decl = cl.tools.match_dtype_to_c_struct(context.devices[0], "cell", np_dtype)
    return (np_dtype, dtype, c_decl)

  @classmethod
  def get_empty_data(cls, state_class):
    return (-1,-1,-1,-1,-1,-1,-1,-1)+state_class.get_empty_data()

  @classmethod
  def create_initialized(cls, **kwargs):
    cell = cls(kwargs["data"], kwargs["index"])
    cell.neighs = kwargs["neighbourhood"].create_empty()
    return cell

  @property
  def state(self):
    offset = 8
    return tuple([self.data[offset+i] for i in range(len(self.data)-offset)])

  @state.setter
  def state(self, state):
    # copy state data to cell data with offset of neighours
    offset = 8
    for i in range(len(state)):
      self.data[offset+i] = state[i]

