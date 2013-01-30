from random import random
from random import randint

class State(object):
  @classmethod
  def create_state(cls):
    raise NotImplementedError("create_state method of state class is not implemented")

  @classmethod
  def create_random_state(cls):
    raise NotImplementedError("create_random_state method of state class is not implemented")

  @classmethod
  def initial_state_value(cls):
    raise NotImplementedError("initial_state_value method of state class is not implemented")

class BinaryState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.alive = cls.initial_state_value()
    return state

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.alive = random() < 0.5
    return state

  @classmethod
  def initial_state_value(cls):
    return False

class ColorState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.rgb = cls.initial_state_value()
    return state

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.rgb = (randint(0,255),randint(0,255),randint(0,255))
    return state

  @classmethod
  def initial_state_value(cls):
    return (0,0,0)

class ColorTopologyState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.rgb, state.wants_divide, state.wants_grow = cls.initial_state_value()
    return state

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.rgb = (randint(0,255),randint(0,255),randint(0,255))
    state.wants_divide = random() < 0.5
    state.wants_grow = random() < 0.5
    return state

  @classmethod
  def initial_state_value(cls):
    return ((0,0,0), False, False)

class ChemicalState(State):
  @classmethod
  def create_state(cls):
    state = cls()
    state.chemicals = cls.initial_state_value(cls)
    return state

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.chemicals = (random(), random(), random())
    return state

  @classmethod
  def initial_state_value(cls):
    return (.0,.0,.0)

