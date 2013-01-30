class State(object):
  @classmethod
  def create_state(cls):
    raise NotImplementedError("create_state method of state class is not implemented")

class BinaryState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.alive = True
    return state

class ColorState(State):
  @classmethod
  def create_state(cls):
    state = cls
    state.rgb = [0,0,0]
    return state

class ColorTopologyState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.rgb = [0,0,0]
    state.wants_divide = False
    state.wants_grow = False
    return state

class ChemicalState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.chemicals = [.0,.0,.0]
    return state

