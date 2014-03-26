from __future__ import print_function
from cellular_automata.cells.regular import SquareCell
from cellular_automata.cells.regular import VariableSquareCell
from cellular_automata.lattices.base import Lattice
from multiprocessing.pool import ThreadPool

from re import match
from utils.nonrecursivepickler import NonrecursivePickler
from cPickle import Pickler
from math import sqrt

import logging


class SquareLattice(Lattice):
    """
    This lattice is using Square Cells to construct 2 dimensional grid of
    square cells that don't change their topology, size or other properties

    Cells are stored in dictionary where coordinates of cells is key value.
    """

    def __init__(self):
        Lattice.__init__(self)
        self.cells = None
        self.resolution = 0
        self.check_pre_post_methods()
        self.energy_history = []

        self.pool = ThreadPool()

    def energy(self):
        return sqrt(sum(map(lambda cell: cell.energy, self.cells.values())))

    def save_energy(self):
        energy = self.energy()
        self.energy_history.append(energy)

    def average_energy_window(self, window_size):
        return sum(self.energy_history[-window_size:]) / float(window_size)

    def energy_variance(self, window_size):
        if len(self.energy_history) < window_size or window_size == 0:
            return len(self.cells.values())*255

        energies = self.energy_history[-window_size:]
        average_energy = self.average_energy_window(window_size)

        average_difference = map(lambda e: (e - average_energy) ** 2, energies)
        energy_variance = sqrt(sum(average_difference) / float(window_size))
        return energy_variance

    def energy_difference(self):
        """This method returns sum of differences of cells from their previous
        state.
        """
        if len(self.energy_history) <= 0:
            return len(self.cells.values())*255
        else:
            return self.energy_history[-1]

    @classmethod
    def create_initialized(cls, conf):
        lattice = cls()

        # set lattice dimensions
        lattice.width = int(conf["lattice"]["width"])
        lattice.height = int(conf["lattice"]["height"])
        lattice.resolution = int(conf["lattice"]["resolution"])

        # supply lattice with neighbourhood class
        lattice.neighbourhood = conf["cells"]["neighbourhood"]

        # prepare the brain of the CA
        rule_class = conf["cells"]["rule"]
        border = lattice.read_border(conf)
        if conf.has_key("chemicals_vector_length") and conf.has_key("internal_vector_length"):
            lattice.rule = rule_class(int(conf["chemical_vector_length"]), int(conf["internal_vector_length"]))
        else:
            lattice.rule = rule_class()
        lattice.rule.set_border(border)

        if "initial_weights" in conf.keys():
            weights = eval(conf["network"]["weights"])
            lattice.rule.set_weights(weights)

        # cells are just carrying state, right? What kind of state? Here it is!
        lattice.cell_state_class = conf["cells"]["state"]

        # all set, let's create all cells
        lattice.cells = lattice.initialize_lattice_cells()
        return lattice

    def save_configuration(self, file_name):
        """ export all lattice properties and cells into file for later use"""
        with open(file_name, 'w') as f:
            pkl = NonrecursivePickler(f)
            pkl.dump(self)

    def initialize_lattice_cells(self):
        cells = self.create_cells(self.rule)
        self.initialize_neighbours(cells)
        return cells

    def create_cells(self, rule):
        cells = {}
        for x in range(0, self.width, self.resolution):
            for y in range(0, self.height, self.resolution):
                cells[(x, y)] = SquareCell.create_initialized(
                    rule,
                    self.neighbourhood,
                    self.cell_state_class)
                coordinates = (x + self.resolution / 2, y + self.resolution / 2)
                cells[(x, y)].position = coordinates
                cells[(x, y)].radius = self.resolution / 2
        return cells

    def initialize_neighbours(self, cells):
        for (x, y), cell in cells.items():
            neighs = self.neighbourhood.gather_neighbours(cells,
                                                          self.resolution, x, y)
            cells[(x, y)].set_neighbours(neighs)

    # set state of particular cell
    def set_state_of_cell(self, state, x, y):
        if x >= 0 or x < self.width or y >= 0 or y < self.height:
            self.cells[(x, y)].state = state

    def next_step(self):
        '''This is THE method for going from one state of all cell to next state.
        Also, there is need to dynamically add some particular calculations that
        needs to be done before or after state of cell has changed.

        Because of that, this method finds all methods of this instance that has
        special names and executes them.

        Method names with following prefixes are recognized:
          def pre_*_method(self) -> executes before cells state changes
          def post_*_method(self) -> executes after cells state changes

        Asterisk is replaced by custom name of method.

        To add new methods you can either use duck punching or inherit and extend
        this class or its descendants.

        To avoid searching for methods each time we want next step, there's update
        method for refreshing list of pre and post methods with method called

          self.check_pre_post_methods()

        '''

        # execute all pre methods
        map(lambda method: getattr(self, method)(), self.pre_methods)

        # change state of cells to next state
        self.pool.map(lambda cell: cell.compute_next_state(), self.cells.values())
        self.pool.map(lambda cell: cell.apply_next_state(), self.cells.values())

        # execute all pre methods
        map(lambda method: getattr(self, method)(), self.post_methods)


        self.time += 1

    def check_pre_post_methods(self):
        """This method check all instance methods, finds methods that should be
        executed before going to next step and after this step. This methods are
        stored in list and executed later, when self.next_step() method is called

        This method should be called just in case of duck punching.
        """
        pre_ptrn = "pre_.+_method"
        self.pre_methods = [m for m in dir(self) if
                            callable(getattr(self, m)) and match(pre_ptrn, m)]

        post_ptrn = "post_.+_method"
        self.post_methods = [m for m in dir(self) if
                             callable(getattr(self, m)) and match(post_ptrn, m)]

    def post_energy_variance_method(self):
        self.save_energy()

    def run(self, stop_criterion, replay_file=None):
        if replay_file is None:
          self.run_without_record(stop_criterion)
        else:
          self.run_with_record(stop_criterion, replay_file)

    def run_without_record(self, stop_criterion):
        log = logging.getLogger("LATTICE")
        log.info("starting lattice run")
        try:
            while stop_criterion.should_run(self):
                self.next_step()
        except Exception as e:
            log.exception("exception occured during lattice run")
            log.exception(e)

    def run_with_record(self, stop_criterion, replay_file):
        log = logging.getLogger("LATTICE")
        data = (stop_criterion.max_time+1)*[None]
        try:
            while stop_criterion.should_run(self):
                self.next_step()
                states_data = len(self.cells)*[None]
                for cell in self.cells.values():
                    pos = cell.top_left_corner
                    index = pos[0]/self.resolution + (pos[1]/self.resolution)*(self.width/self.resolution)
                    states_data[index] = cell.state.to_dict()
                data[self.time] = states_data
        except:
            log.exception("exception occured during lattice run")
        finally:
            log.info("saving data from run into {}".format(replay_file))
            self.save_replay(data, replay_file)

    def save_replay(self, data, replay_file):
        replay = {}
        replay["width"] = self.width / self.resolution
        replay["height"] = self.height / self.resolution
        replay["resolution"] = self.resolution
        replay["length"] = self.time
        replay["data"] = data

        with open(replay_file, "w") as fp:
            pkl = Pickler(fp)
            pkl.dump(replay)

            log = logging.getLogger("LATTICE")
            log.debug("Lattice run saved into replay")

    def get_lattice(self):
        return self.cells.values()


class DiffusionSquareLattice(SquareLattice):
    '''This class just extends Square Lattice and adds diffusion process
    chemicals in cells. We implements this by 2 pass gaussian blur filter on chemicals.
    '''

    def first_pass(self):
        '''First horizontal pass of gaussian blur filter'''
        map(lambda cell: self.gaussian_blur_pass(cell, ["west", "east"]),
            self.cells.values())

    def second_pass(self):
        '''Second vertical pass of gaussian blur filter'''
        map(lambda cell: self.gaussian_blur_pass(cell, ["north", "south"]),
            self.cells.values())

    def gaussian_blur_pass(self, cell, directions):
        '''Apply horizontal or vertical pass of gaussian blur filter.
        Take chemicals from neighbours in selected directions,
        combine them together with cell chemicals in fllowing way

                            chems1 + 2*own_chems + chems2
              cell.chems = -------------------------------
                                          4

        Chemicals should be weighted acordingly to common border width between cells,
        but in this case, we have regular cells with same size, weighting is not
        neccessary.
        '''
        chems = [iter(cell.neighs[direction]).next().state.chemicals for
                 direction in directions if len(cell.neighs[direction]) == 1]
        chems.append(map(lambda x: x * 2, cell.state.chemicals))
        chems = reduce(lambda x, y: map(sum, zip(x, y)), chems)
        cell.state.chemicals = map(lambda x: x / 4, chems)

    def pre_diffusion_method(self):
        self.first_pass()
        self.second_pass()


class VariableSquareLattice(SquareLattice):
    '''Variable Square Lattice is lattice which cells can change size,
    change neighbour connections accordingly to changes in sizes.
    Cells can be merged together and divided into 4 smaller cells

    Variable Square Lattice is using Variable Square Cells that can change size.
    However this lattice is still regular from angular point of view. That's reason
    why is in module of Equiangular lattices.

    Cells are stored in dictionary based on their current coordinates on grid.
    '''

    def create_cells(self, rule):
        cells = {}
        for x in range(0, self.width, self.resolution):
            for y in range(0, self.height, self.resolution):
                coordinates = (x + self.resolution / 2, y + self.resolution / 2)
                cells[coordinates] = VariableSquareCell.create_initialized(
                    rule,
                    self.neighbourhood,
                    self.cell_state_class)

                cells[coordinates].position = coordinates
                cells[coordinates].radius = self.resolution / 2
        return cells

    def pre_handle_growing_cells_method(self):
        growing_cells = [cell for cell in self.cells.values() if
                         cell.wants_grow()]
        for growing_cell in growing_cells:
            if growing_cell in self.cells.values(): # additional check if cell wasn't already merged
                cells_to_merge = growing_cell.grow()
                if cells_to_merge is None:
                    return
                changes = self.merge_cells(cells_to_merge)
                self.handle_change_in_cells(changes)

    def pre_handle_dividing_cells_method(self):
        dividing_cells = [cell for cell in self.cells.values() if
                          cell.wants_divide()]
        for dividing_cell in dividing_cells:
            changes = self.divide(dividing_cell)
            self.handle_change_in_cells(changes)

    def handle_change_in_cells(self, changes):
        if changes is not None:
            cells_to_remove, cells_to_add = changes
            self.remove_cells(cells_to_remove)
            self.add_cells(cells_to_add)

    def add_cells(self, list_of_cells_to_add):
        for cell_to_add in list_of_cells_to_add:
            self.cells[cell_to_add.position] = cell_to_add

    def remove_cells(self, list_of_cells_to_remove):
        for cell_to_remove in list_of_cells_to_remove:
            try:
                del self.cells[cell_to_remove.position]
            except KeyError as e:
                print("cell at {0} not in self.cells".format(
                    cell_to_remove.position))

    def merge_cells(self, cells_to_merge):
        new_cell = self.create_new_cell(cells_to_merge)
        self.put_new_cell_into_neighbourhood(new_cell, cells_to_merge)
        return cells_to_merge, [new_cell]

    def create_new_cell(self, cells_to_merge):
        new_cell = VariableSquareCell.create_initialized(
            self.rule,
            self.neighbourhood,
            self.cell_state_class)
        new_cell.position = self.interpolate_center(cells_to_merge)
        new_cell.size = len(cells_to_merge) * cells_to_merge[0].size
        new_cell.radius = cells_to_merge[0].radius * 2
        return new_cell

    def put_new_cell_into_neighbourhood(self, new_cell, cells_to_merge):
        self.set_neighbours_of_new_cell(new_cell, cells_to_merge)
        self.update_surrounding_neighbourhood(new_cell, cells_to_merge)

    def set_neighbours_of_new_cell(self, new_cell, cells_to_merge):
        new_neighbours = self.neighbourhood.create_empty()
        for direction in new_neighbours.keys():
            new_neighbours[direction] = set(
                [neigh for cell in cells_to_merge for neigh in
                 cell.neighs[direction] if neigh not in cells_to_merge])
        new_cell.set_neighbours(new_neighbours)

    def update_surrounding_neighbourhood(self, new_cell, cells_to_merge):
        for direction, neighs in new_cell.neighs.items():
            for neigh in neighs:
                self.remove_old_neighbors(neigh, direction, cells_to_merge)
                self.add_new_neighbors(neigh, direction, [new_cell])

    @staticmethod
    def remove_old_neighbors(cell, direction, cells_to_remove):
        opposite_direction = VariableSquareLattice.reverse_direction(direction)
        for old_neigh in cells_to_remove:
            if old_neigh in cell.neighs[opposite_direction]:
                cell.neighs[opposite_direction].remove(old_neigh)

    @staticmethod
    def add_new_neighbors(cell, direction, cells_to_add):
        opposite_direction = VariableSquareLattice.reverse_direction(direction)
        cell.neighs[opposite_direction].update(cells_to_add)

    def divide(self, cell):
        # create 4 new cells
        cell_nw = VariableSquareCell.create_initialized(self.rule,
                                                        self.neighbourhood,
                                                        self.cell_state_class)
        cell_ne = VariableSquareCell.create_initialized(self.rule,
                                                        self.neighbourhood,
                                                        self.cell_state_class)
        cell_sw = VariableSquareCell.create_initialized(self.rule,
                                                        self.neighbourhood,
                                                        self.cell_state_class)
        cell_se = VariableSquareCell.create_initialized(self.rule,
                                                        self.neighbourhood,
                                                        self.cell_state_class)

        cell_nw.size = cell.size / 4
        cell_ne.size = cell.size / 4
        cell_sw.size = cell.size / 4
        cell_se.size = cell.size / 4

        # position
        half_radius = cell.radius / 2

        cell_nw.position = (cell.x - half_radius, cell.y - half_radius)
        cell_nw.radius = half_radius
        cell_ne.position = (cell.x + half_radius, cell.y - half_radius)
        cell_ne.radius = half_radius
        cell_sw.position = (cell.x - half_radius, cell.y + half_radius)
        cell_sw.radius = half_radius
        cell_se.position = (cell.x + half_radius, cell.y + half_radius)
        cell_se.radius = half_radius

        # create neighbor connections
        cell_nw.neighs["south"] = set([cell_sw])
        cell_nw.neighs["east"] = set([cell_ne])
        cell_ne.neighs["south"] = set([cell_se])
        cell_ne.neighs["west"] = set([cell_nw])
        cell_sw.neighs["north"] = set([cell_nw])
        cell_sw.neighs["east"] = set([cell_se])
        cell_se.neighs["north"] = set([cell_ne])
        cell_se.neighs["west"] = set([cell_sw])

        new_cells = {}
        new_cells["north"] = [cell_nw, cell_ne]
        new_cells["east"] = [cell_ne, cell_se]
        new_cells["south"] = [cell_se, cell_sw]
        new_cells["west"] = [cell_nw, cell_sw]

        for direction, direction_neighs in cell.neighs.items():
            for direction_neigh in direction_neighs:
                for new_cell in new_cells[direction]:
                    if self.is_neighbor_with(direction_neigh, new_cell):
                        new_cell.neighs[direction].add(direction_neigh)

        # now we have new cells with correct neighs.
        # this time we have to update rest of the neighborhood
        for new_cell in [cell_nw, cell_ne, cell_sw, cell_se]:
            self.update_surrounding_neighbourhood(new_cell, [self])

        return [cell], [cell_nw, cell_ne, cell_sw, cell_se]

    @staticmethod
    def is_neighbor_with(cell1, cell2):
        cell1_left = cell1.x - cell1.radius
        cell1_right = cell1.x + cell1.radius
        cell2_left = cell2.x - cell2.radius
        cell2_right = cell2.x + cell2.radius

        cell1_top = cell1.y - cell1.radius
        cell1_bottom = cell1.y + cell1.radius
        cell2_top = cell2.y - cell2.radius
        cell2_bottom = cell2.y + cell2.radius

        if cell1_left < cell2_left or cell2_right < cell1_left:
            return False
        elif cell1_bottom < cell2_top or cell2_bottom < cell1_top:
            return False
        return True

    @staticmethod
    def interpolate_center(cells):
        one = cells[0]
        opposite = cells[2]
        x = (one.x + opposite.x) / 2
        y = (one.y + opposite.y) / 2
        return x, y

    @staticmethod
    def turn_right(direction):
        if direction == "north":
            return "east"
        elif direction == "east":
            return "south"
        elif direction == "south":
            return "west"
        elif direction == "west":
            return "north"
        else:
            raise Exception(direction + " is wrong direction to turn right!")

    @staticmethod
    def reverse_direction(direction):
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

