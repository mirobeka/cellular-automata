class Cell(object):
  def __init__(self):
    self.rule = None
    self.age = 0
    self._position = (0,0)
    self._radius = 0
    self.initialize_state()

  @classmethod
  def createInitialized(cls, rule, neighbourhood, state_class):
    cell = cls()
    cell.rule = rule
    cell.neighs = neighbourhood.create_empty()
    cell.state = state_class.create_state()
    return cell

  @classmethod
  def createEmpty(cls):
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
  def position(self, newPos):
    if type(newPos) == tuple and len(newPos) == 2:
      self._position = newPos
      self._tlc = tuple(x-self.radius for x in newPos)
      self._brc = tuple(x+self.radius for x in newPos)
    else:
      raise Exception("wrong position argument: {}".format(newPos))

  def toDict(self):
    raise NotImplementedError("method toYAML of cell is not implemented")

  @property
  def boundingBox(self):
    return self._tlc + self._brc

  @property
  def topLeftCorner(self):
    return self._tlc

  @topLeftCorner.setter
  def topLeftCorner(self, newPos):
    self.position = tuple(x+self.radius for x in newPos)

  @property
  def bottomRightCorner(self):
    return self._brc

  @bottomRightCorner.setter
  def bottomRightCorner(self, newPos):
    self.position = tuple(x-self.radius for x in newPos)

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

  def getNeighbors(self):
    return self.neighs
