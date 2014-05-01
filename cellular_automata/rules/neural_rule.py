from cellular_automata.rules.base import Rule
from pybrain.tools.shortcuts import buildNetwork
import numpy as np
import logging

log = logging.getLogger("RULE")

class HardCodedRule1(Rule):
    """Programatically written rule for dividing space into 2 halves"""

    def get_next_state(self, cell, neighbours):
        new_state = cell.state.create_state()
        if cell.position[0] <= 200:
            new_state.grayscale = min(cell.state.grayscale+1, 254)
        else:
            new_state.grayscale = max(cell.state.grayscale-1, 0)

        return new_state

    def set_border(self, border=None):
        self.border = border

    def set_weights(self, new_weights):
        pass

    def get_weights(self):
        return None

class HardCodedRule2(Rule):
    """Programatically written rule for dividing space into 2 halves"""

    def get_next_state(self, cell, neighbours):
        new_state = cell.state.create_state()

        west = self.get_neighbour_state_value(cell, neighbours, "west")
        east = self.get_neighbour_state_value(cell, neighbours, "east")

        new_state.internal = np.tanh(west + east)
        if new_state.internal < 0:
            new_state.grayscale = 255
        else:
            new_state.grayscale = 0

        #new_state.grayscale = max(min(int(255 - ((new_state.internal+1)/2)*255), 255), 0)

        return new_state

    def get_neighbour_state_value(self, cell, neighbours, direction):
        if len(neighbours[direction]) <= 0:
            return self.get_border_value(cell.position, direction)[0]
        else:
            return iter(neighbours[direction]).next().state.internal

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border

class HardCodedRule3(Rule):
    def __init__(self, internal_state_vector_length=1):
        self.internal_state_vector_length = internal_state_vector_length
        self.input_layer_length = 5 * self.internal_state_vector_length
        self.hidden_layer_length = self.input_layer_length + 2
        self.output_layer_length = self.internal_state_vector_length+1
        self.randomize_weights()

    def randomize_weights(self):
        number_of_weights = self.total_number_of_weights()
        weights = np.random.rand(number_of_weights)
        self.set_weights(weights)

    def total_number_of_weights(self):
        """Return total number of weights that are used"""
        return (self.input_layer_length + 1) * self.hidden_layer_length + (
            self.hidden_layer_length + 1) * self.output_layer_length + self.output_layer_length

    def set_weights(self, new_weights):
        """Weights we are evolving are passed to neural network by this function.
        list of weight values are sorted like this.

        input -> hidden layer weights = ( 5 * state vector + 1 ) * hidden layer length
        hidden -> output layer weights = ( hidden l. length + 1 ) * ( state vector + color vector )
        """

        self.weights = new_weights
        if type(new_weights) is list:
            new_weights = np.array(new_weights)

        first_slice = (self.input_layer_length + 1) * self.hidden_layer_length
        self.theta1 = np.array(new_weights[:first_slice])
        self.theta1.shape = (
            self.hidden_layer_length, self.input_layer_length + 1)

        second_slice = (self.hidden_layer_length + 1) * self.output_layer_length
        self.theta2 = new_weights[first_slice:first_slice + second_slice]
        self.theta2.shape = (
            self.output_layer_length, self.hidden_layer_length + 1)

    def get_weights(self):
        return self.weights

    def get_next_state(self, cell, neighbours):
        # get input vector from neighbours
        input_vector = self.get_input_vector(cell, neighbours)

        # get hidden layer
        a1 = np.insert(input_vector, 0, 1)
        hidden_layer = np.tanh(np.dot(self.theta1, a1))

        # get output layer
        a2 = np.insert(hidden_layer, 0, 1)
        out_vector = np.tanh(np.dot(self.theta2, a2))

        # set new internal state of cell
        new_internal_state = out_vector[0]
        if new_internal_state <= 0.5:
            new_color = 0.1
        else:
            new_color = 0.9

        # finally create new state
        new_state = cell.state.create_state()
        new_state.internal = new_internal_state
        new_state.grayscale = max(min(int(new_color * 255), 255), 0)
        return new_state

    def get_input_vector(self, cell, neighbours):
        """ Here we are dealing with just one neighbour per direction. It's Square
        Lattice so there is just one neighbour per direction.
        """
        input_list = []
        input_list.append(cell.state.internal)
        for direction in ["north", "east", "south", "west"]:
            if len(neighbours[direction]) == 0:
                border_value = self.get_border_value(cell.position, direction)
                input_list.extend(border_value)
            else:
                input_list.append(
                    iter(neighbours[direction]).next().state.internal)

        if len(input_list) != self.input_layer_length:
            print("{0} != {1}".format(len(input_list), self.input_layer_length))
            raise Exception("invalid input layer length")
        return np.array(input_list)

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border

class FeedForwardNetworkMoore(Rule):
    def __init__(self, internal_state_vector_length=1):
        self.internal_state_vector_length = internal_state_vector_length
        self.input_layer_length = 9 * self.internal_state_vector_length
        self.hidden_layer_length = self.input_layer_length - 4
        self.output_layer_length = self.internal_state_vector_length
        self.randomize_weights()

    def randomize_weights(self):
        number_of_weights = self.total_number_of_weights()
        weights = np.random.rand(number_of_weights)
        self.set_weights(weights)

    def total_number_of_weights(self):
        """Return total number of weights that are used"""
        return (self.input_layer_length + 1) * self.hidden_layer_length + (
            self.hidden_layer_length + 1) * self.output_layer_length

    def set_weights(self, new_weights):
        """Weights we are evolving are passed to neural network by this function.
        list of weight values are sorted like this.

        input -> hidden layer weights = ( 5 * state vector + 1 ) * hidden layer length
        hidden -> output layer weights = ( hidden l. length + 1 ) * ( state vector + color vector )
        """

        self.weights = new_weights
        if type(new_weights) is list:
            new_weights = np.array(new_weights)

        first_slice = (self.input_layer_length + 1) * self.hidden_layer_length
        self.theta1 = np.array(new_weights[:first_slice])
        self.theta1.shape = (
            self.hidden_layer_length, self.input_layer_length + 1)

        second_slice = (self.hidden_layer_length + 1) * self.output_layer_length
        self.theta2 = new_weights[first_slice:first_slice + second_slice]
        self.theta2.shape = (
            self.output_layer_length, self.hidden_layer_length + 1)

    def get_weights(self):
        return self.weights

    def get_next_state(self, cell, neighbours):
        # get input vector from neighbours
        input_vector = self.get_input_vector(cell, neighbours)

        # get hidden layer
        a1 = np.insert(input_vector, 0, 1)
        hidden_layer = np.tanh(np.dot(self.theta1, a1))

        # get output layer
        a2 = np.insert(hidden_layer, 0, 1)
        out_vector = np.tanh(np.dot(self.theta2, a2))

        # set new internal state of cell
        new_internal_state = out_vector[0]
        new_grayscale_color = 255*(new_internal_state+1)/2

        # finally create new state
        new_state = cell.state.create_state()
        new_state.internal = new_internal_state
        new_state.grayscale = max(min(int(new_grayscale_color), 255), 0)
        return new_state

    def get_input_vector(self, cell, neighbours):
        """ Here we are dealing with just one neighbour per direction. It's Square
        Lattice so there is just one neighbour per direction.
        """
        input_list = []
        input_list.append(cell.state.internal)
        for direction in ["north","northeast", "east", "southeast", "south", "southwest", "west", "northwest"]:
            if len(neighbours[direction]) == 0:
                border_value = self.get_border_value(cell.position, direction)
                input_list.extend(border_value)
            else:
                input_list.append(
                    iter(neighbours[direction]).next().state.internal)

        if len(input_list) != self.input_layer_length:
            print("{0} != {1}".format(len(input_list), self.input_layer_length))
            raise Exception("invalid input layer length")
        return np.array(input_list)

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border

class FeedForwardNetwork(Rule):
    def __init__(self, internal_state_vector_length=1):
        self.internal_state_vector_length = internal_state_vector_length
        self.input_layer_length = 5 * self.internal_state_vector_length
        self.hidden_layer_length = self.input_layer_length - 2
        self.output_layer_length = self.internal_state_vector_length
        self.randomize_weights()

    def randomize_weights(self):
        number_of_weights = self.total_number_of_weights()
        weights = np.random.rand(number_of_weights)
        self.set_weights(weights)

    def total_number_of_weights(self):
        """Return total number of weights that are used"""
        return (self.input_layer_length + 1) * self.hidden_layer_length + (
            self.hidden_layer_length + 1) * self.output_layer_length

    def set_weights(self, new_weights):
        """Weights we are evolving are passed to neural network by this function.
        list of weight values are sorted like this.

        input -> hidden layer weights = ( 5 * state vector + 1 ) * hidden layer length
        hidden -> output layer weights = ( hidden l. length + 1 ) * ( state vector + color vector )
        """

        self.weights = new_weights
        if type(new_weights) is list:
            new_weights = np.array(new_weights)

        first_slice = (self.input_layer_length + 1) * self.hidden_layer_length
        self.theta1 = np.array(new_weights[:first_slice])
        self.theta1.shape = (
            self.hidden_layer_length, self.input_layer_length + 1)

        second_slice = (self.hidden_layer_length + 1) * self.output_layer_length
        self.theta2 = new_weights[first_slice:first_slice + second_slice]
        self.theta2.shape = (
            self.output_layer_length, self.hidden_layer_length + 1)

    def get_weights(self):
        return self.weights

    def get_next_state(self, cell, neighbours):
        # get input vector from neighbours
        input_vector = self.get_input_vector(cell, neighbours)

        # get hidden layer
        a1 = np.insert(input_vector, 0, 1)
        hidden_layer = np.tanh(np.dot(self.theta1, a1))

        # get output layer
        a2 = np.insert(hidden_layer, 0, 1)
        out_vector = np.tanh(np.dot(self.theta2, a2))

        # set new internal state of cell
        new_internal_state = out_vector[0]
        new_grayscale_color = 255*(new_internal_state+1)/2

        # finally create new state
        new_state = cell.state.create_state()
        new_state.internal = new_internal_state
        new_state.grayscale = max(min(int(new_grayscale_color), 255), 0)
        return new_state

    def get_input_vector(self, cell, neighbours):
        """ Here we are dealing with just one neighbour per direction. It's Square
        Lattice so there is just one neighbour per direction.
        """
        input_list = []
        input_list.append(cell.state.internal)
        for direction in ["north", "east", "south", "west"]:
            if len(neighbours[direction]) == 0:
                border_value = self.get_border_value(cell.position, direction)
                input_list.extend(border_value)
            else:
                input_list.append(
                    iter(neighbours[direction]).next().state.internal)

        if len(input_list) != self.input_layer_length:
            print("{0} != {1}".format(len(input_list), self.input_layer_length))
            raise Exception("invalid input layer length")
        return np.array(input_list)

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border
    

class FullyInformed(Rule):
    """This rule takes as input for neural network it's position and based
    on actual position of a cell, it returns the right color. This is fully informed
    method that is not scalable for any other solution than just this one (that
    means this particular pattern).
    """

    def set_weights(self, new_weights):
        self.theta1 = np.array(new_weights[0:12])
        self.theta1.shape = (4,3)
        self.theta2 = np.array(new_weights[13:28])
        self.theta2.shape = (3,5)
        self.theta3 = np.array(new_weights[29:33])
        self.theta3.shape = (1,4)

    def total_number_of_weights(self):
        return 33

    def get_next_state(self, cell, neighs):
        input_vector = [cell.x, cell.y]
        
        a1 = np.insert(input_vector, 0, 1)
        hidden_layer1 = np.tanh(np.dot(self.theta1, a1))

        a2 = np.insert(hidden_layer1, 0, 1)
        hidden_layer2 = np.tanh(np.dot(self.theta2, a2))

        a3 = np.insert(hidden_layer2, 0, 1)
        new_color = np.tanh(np.dot(self.theta3, a3))

        # map new color to interval <0, 355>
        grayscale = int((new_color[0]/2.0 + 0.5)*255)

        new_state = cell.state.create_state()
        new_state.chemicals = cell.state.chemicals
        new_state.internal = cell.state.internal
        new_state.grayscale = grayscale

        return new_state

    def set_border(self, border=None):
        self.border = border

class ANNColorRule(Rule):
    """This rule is implementing own neural network that takes chemicals of
    cells and their internal states as input then calculate one hidden layer
    and then also takes other input and uses this input in activating other
    neurons in hidden layer. Then outputs cell chemical and state vector.
    """

    def __init__(self, chemicals_vector_length=1,
                 internal_state_vector_length=1):
        self.chemicals_vector_length = chemicals_vector_length
        self.internal_state_vector_length = internal_state_vector_length
        self.input_layer_length = 4 * self.chemicals_vector_length + self.internal_state_vector_length
        self.hidden_layer_length = int(self.input_layer_length * 1.5)
        self.output_layer_length = self.internal_state_vector_length + self.chemicals_vector_length
        self.randomize_weights()

    def randomize_weights(self):
        number_of_weights = self.total_number_of_weights()
        weights = np.random.rand(number_of_weights)
        self.set_weights(weights)

    def total_number_of_weights(self):
        """Return total number of weights that are used"""
        return (self.input_layer_length + 1) * self.hidden_layer_length + (
            self.hidden_layer_length + 1) * self.output_layer_length + self.output_layer_length

    def set_weights(self, new_weights):
        """Weights we are evolving are passed to neural network by this function.
    list of weight values are sorted like this.

        input -> hidden layer weights = (4*chemical vector + 1*state vector + 1)* hidden layer length
        hidden -> output layer weights = (hidden l. length + 1) * (1*state vector + 1*chemical vector)
        output -> cell color weights = (1*state vector + 1*chemical vector + 1) * 1

    So actually we are using 3 types of weights for our network
    """
        self.weights = new_weights
        if type(new_weights) is list:
            new_weights = np.array(new_weights)
        first_slice = (self.input_layer_length + 1) * self.hidden_layer_length
        self.theta1 = np.array(new_weights[:first_slice])
        self.theta1.shape = (
            self.hidden_layer_length, self.input_layer_length + 1)

        second_slice = (self.hidden_layer_length + 1) * self.output_layer_length
        self.theta2 = new_weights[first_slice:first_slice + second_slice]
        self.theta2.shape = (
            self.output_layer_length, self.hidden_layer_length + 1)

        last_slice = self.output_layer_length + 1
        self.theta3 = new_weights[-last_slice:]
        self.theta3.shape = (1, self.output_layer_length + 1)

    def get_weights(self):
        return self.weights

    def get_next_state(self, cell, neighbours):
        # get input vector from neighbours
        input_vector = self.get_input_vector(cell, neighbours)

        # get hidden layer
        a1 = np.insert(input_vector, 0, 1)
        hidden_layer = np.tanh(np.dot(self.theta1, a1))

        # get output layer
        a2 = np.insert(hidden_layer, 0, 1)
        out_vector = np.tanh(np.dot(self.theta2, a2))

        # set new internal state and chemicals of cell
        new_internal_state = out_vector[:self.internal_state_vector_length]
        new_chemicals = out_vector[-self.chemicals_vector_length:]

        # add previous chemical concentration
        new_chemicals += cell.state.chemicals

        # get new color of cell
        color_vector = np.append(new_internal_state, new_chemicals)
        a3 = np.insert(color_vector, 0, 1)
        new_color = (np.tanh(np.dot(self.theta3, a3)) + 1) / 2

        # finally create new state
        new_state = cell.state.create_state()
        new_state.chemicals = new_chemicals
        new_state.internal = new_internal_state
        new_state.grayscale = int(new_color * 255)
        return new_state

    def get_input_vector(self, cell, neighbours):
        """ Here we are dealing with just one neighbour per direction. It's Square
        Lattice so there is just one neighbour per direction.
        """
        input_list = []
        input_list.extend(cell.state.internal)
        for direction in ["north", "east", "south", "west"]:
            if len(neighbours[direction]) == 0:
                border_value = self.get_border_value(cell.position, direction)
                input_list.extend(border_value)
            else:
                input_list.extend(
                    iter(neighbours[direction]).next().state.chemicals)

        if len(input_list) != self.input_layer_length:
            print("{0} != {1}".format(len(input_list), self.input_layer_length))
            raise Exception("invalid input layer length")
        return np.array(input_list)

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border
