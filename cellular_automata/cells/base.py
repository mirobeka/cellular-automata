class Cell(object):
  def __init__(self, rule):
    self.rule = rule
    self.neighs = None
    self.age = 0
    self._position = (0,0)
    self.createState()

  def createState(self):
    self.state = {}
    self.state["current"] = None
    self.state["next"] = None

  # few property getters and setters
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, newPos):
    if type(newPos) == tuple and len(newPos) == 2:
      self._position = newPos
    else:
      raise Exception("wrong position argument: {}".format(newPos))

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
    self.state["next"] = self.rule.getNextState(self, self.neighs)

  def applyNextState(self):
    self.state["current"] = self.state["next"]
    self.age += 1

  def getState(self):
    return self.state["current"]

  def setState(self, state):
    self.state["current"] = state
  
  def getNeighbors(self):
    return self.neighs
