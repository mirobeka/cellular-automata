from random import random
from random import randint
from numpy import array
from numpy import repeat
from numpy.random import rand
import numpy as np

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
    state.chemicals = cls.initial_state_value()
    return state

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.chemicals = (random(), random(), random())
    return state

  @classmethod
  def initial_state_value(cls):
    return (random(), random(), random())
    # return (.0,.0,.0)

class ChemicalInternalGrayscaleState(State):
  '''This state contains chemical vector of length 3, internal state vector
  of length 3 and one grayscale value in interval [0,255]
  '''
  dtype = [
    ("grayscale",np.int),
    ("ch0",np.float32),("ch1",np.float32),("ch2",np.float32),
    ("st0",np.float32),("st1",np.float32),("st2",np.float32)
  ]

  @classmethod
  def get_empty_data(cls):
    return (128,.0,.0,.0,.0,.0,.0)

  @classmethod
  def create_state(cls):
    state = cls()
    state.chemicals, state.internal, state.grayscale = cls.initial_state_value()
    return state

  @classmethod
  def initial_state_value(cls):
    chemicals = repeat(.0, 3)
    internal = repeat(.0, 3)
    grayscale = 0
    # chemicals = rand(3)
    # internal = rand(3)
    # grayscale = randint(0,255)
    return (chemicals, internal, grayscale)

  @classmethod
  def create_random_state(cls):
    state = cls()
    state.chemicals = rand(3)*2-1
    state.internal = rand(3)*2-1
    state.garyscale = randint(0,255)
    return state
