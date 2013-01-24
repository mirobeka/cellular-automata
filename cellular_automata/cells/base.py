class Cell(object):
  def __init__(self):
    self.rule = None
    self.neighs = None
    self.age = 0
    self._position = (0,0)
    self.createState()

  @classmethod
  def createInitialized(cls, rule):
    cell = cls()
    cell.rule = rule
    return cell

  @classmethod
  def createEmpty(cls):
    return cls()

  def createState(self):
    self._state = {}
    self._state["current"] = None
    self._state["next"] = None

  @property
  def state(self):
    return self._state["current"]

  @state.setter
  def state(self, state):
    self._state["current"] = state

  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, newPos):
    if type(newPos) == tuple and len(newPos) == 2:
      self._position = newPos
    else:
      raise Exception("wrong position argument: {}".format(newPos))

  def toDict(self):
    raise NotImplementedError("method toYAML of cell is not implemented")

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

  def computeNextState(self):
    self._state["next"] = self.rule.getNextState(self, self.neighs)

  def applyNextState(self):
    self.state = self._state["next"]
    self.age += 1

  def getNeighbors(self):
    return self.neighs
