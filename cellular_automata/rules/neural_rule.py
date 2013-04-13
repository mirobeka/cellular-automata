from cellular_automata.rules.base import Rule
import numpy as np


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
        self.hidden_layer_length = self.input_layer_length * 2
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
                border_value = self.get_border_value(direction)
                input_list.extend(border_value)
            else:
                input_list.extend(
                    iter(neighbours[direction]).next().state.chemicals)

        if len(input_list) != self.input_layer_length:
            print("{} != {}".format(len(input_list), self.input_layer_length))
            raise Exception("invalid input layer length")
        return np.array(input_list)

    def get_border_value(self, coords, direction):
        return self.border[coords][direction]

    def set_border(self, border=None):
        self.border = border