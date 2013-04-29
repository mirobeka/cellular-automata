import numpy as np


class Cell(object):
    def __init__(self):
        self.rule = None
        self.age = 0
        self._position = (0, 0)
        self._radius = 0
        self.current_energy = 0
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
        self._state = dict()
        self._state[0] = None
        self._state[1] = None

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._tlc = (self.x - radius, self.y - radius)
        self._brc = (self.x + radius, self.y + radius)

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, energy):
        self._energy = energy

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
            self._tlc = tuple(x - self.radius for x in new_pos)
            self._brc = tuple(x + self.radius for x in new_pos)
        else:
            raise Exception("wrong position argument: {}".format(new_pos))

    @property
    def bounding_box(self):
        return self._tlc + self._brc

    @property
    def top_left_corner(self):
        return self._tlc

    @top_left_corner.setter
    def top_left_corner(self, new_pos):
        self.position = tuple(x + self.radius for x in new_pos)

    @property
    def bottom_right_corner(self):
        return self._brc

    @bottom_right_corner.setter
    def bottom_right_corner(self, new_pos):
        self.position = tuple(x - self.radius for x in new_pos)

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
        self.previous_energy = self.current_energy
        self.current_energy = self.state.euclidean_distance()
        self.energy = abs(self.previous_energy - self.current_energy)
        self.age += 1

    def get_neighbors(self):
        return self.neighs

