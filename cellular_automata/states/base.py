from random import random
from random import randint
from numpy import repeat
from numpy.random import rand
from math import sqrt
import numpy as np


class State(object):
    @classmethod
    def create_state(cls):
        raise NotImplementedError(
            "create_state method of state class is not implemented")

    @classmethod
    def create_random_state(cls):
        raise NotImplementedError(
            "create_random_state method of state class is not implemented")

    @classmethod
    def initial_state_value(cls):
        raise NotImplementedError(
            "initial_state_value method of state class is not implemented")

    def to_dict(self):
        raise NotImplementedError(
            "to_dict method of state instance is not implemented")



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

    def to_dict(self):
        return {"alive": self.alive}

class GrayscaleState(State):
    @classmethod
    def create_state(cls):
        state = cls()
        state.internal, state.grayscale = cls.initial_state_value()
        return state

    @classmethod
    def create_random_state(cls):
        state = cls()
        state.internal = random()
        state.grayscale = randint(0, 255)
        return state

    @classmethod
    def initial_state_value(cls):
        internal = .0
        grayscale = 128
        return internal, grayscale

    def euclidean_distance(self):
        return self.grayscale

    def to_dict(self):
        return {"grayscale": self.grayscale, "state": self.internal}


class ColorState(State):
    @classmethod
    def create_state(cls):
        state = cls()
        state.rgb = cls.initial_state_value()
        return state

    @classmethod
    def create_random_state(cls):
        state = cls()
        state.rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
        return state

    @classmethod
    def initial_state_value(cls):
        return 0, 0, 0

    def euclidean_distance(self):
        return sqrt(sum(map(lambda x: pow(x, 2), self.rgb)))

    def to_dict(self):
        return {"rgb": self.rgb}

class ColorTopologyState(State):
    @classmethod
    def create_state(cls):
        state = cls()
        state.rgb, state.wants_divide, state.wants_grow = cls.initial_state_value()
        return state

    @classmethod
    def create_random_state(cls):
        state = cls()
        state.rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
        state.wants_divide = random() < 0.5
        state.wants_grow = random() < 0.5
        return state

    @classmethod
    def initial_state_value(cls):
        return (0, 0, 0), False, False

    def euclidean_distance(self):
        return sqrt(sum(map(lambda x: pow(x, 2), self.rgb)))

    def to_dict(self):
        return {"rgb":self.rgb, "wants_grow":self.wants_grow, "wants_divide":self.wants_divide}


class ChemicalState(State):
    @classmethod
    def create_state(cls):
        state = cls()
        state.chemicals = cls.initial_state_value()
        return state

    @classmethod
    def create_random_state(cls):
        state = cls()
        state.chemicals = rand(1)
        return state

    @classmethod
    def initial_state_value(cls):
        return rand(1)

    def euclidean_distance(self):
        return abs(self.chemicals)

    def to_dict(self):
        return {"chems":self.chemicals}


class ChemicalInternalGrayscaleState(State):
    """This state contains chemical vector of length 3, internal state vector
    of length 3 and one grayscale value in interval [0,255]
    """

    @classmethod
    def create_state(cls):
        state = cls()
        state.chemicals, state.internal, state.grayscale = cls.initial_state_value()
        return state

    @classmethod
    def initial_state_value(cls):
        chemicals = repeat(.0, 1)
        internal = repeat(.0, 1)
        grayscale = 0
        # chemicals = rand(3)
        # internal = rand(3)
        # grayscale = randint(0,255)
        return chemicals, internal, grayscale

    @classmethod
    def create_random_state(cls):
        state = cls()
        state.chemicals = rand(1) * 2 - 1
        state.internal = rand(1) * 2 - 1
        state.grayscale = randint(0, 255)
        return state

    def euclidean_distance(self):
        distance = 0
        if type(self.chemicals) is list or type(self.chemicals) is np.ndarray:
            distance = sqrt(sum(map(lambda x: x**2, self.internal)))
        else:
            distance = self.internal
        return distance

    def to_dict(self):
        return {"chems":self.chemicals[0], "state": self.internal[0], "grayscale": self.grayscale}


