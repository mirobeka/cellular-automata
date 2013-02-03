from cellular_automata.rules.base import Rule
from pybrain.tools.shortcuts import buildNetwork
import numpy as np

class MLPColorRule(Rule):
  def __init__(self):
    self.state_vector_length = 3

    self.input_layer_length = self.state_vector_length*5
    self.hidden_layer_length = self.input_layer_length*2
    self.output_layer_length = self.state_vector_length

    self.net = buildNetwork(
        self.input_layer_length,
        self.hidden_layer_length,
        self.output_layer_length)

  def get_weights(self):
    return self.net.params

  def set_weights(self, weights):
    new_weights = np.array(weights)
    self.net._setParameters(new_weights)
    print("set weights to = " + str(self.net.params))

  def get_next_state(self, cell, neighbors):
    # collect all data for neural network
    in_vector = self.get_input_vector(cell, neighbors)
    out_vector = self.net.activate(in_vector)
    normalized_values = self.normalize_to_color(out_vector)

    new_state = cell.state.create_state()
    new_state.rgb = tuple(normalized_values)
    return out_vector

  def normalize_to_color(self, out_vector):
    return (out_vector+1)*128-1

  def get_input_vector(self, cell, neighbors):
    in_vector = []
    in_vector.extend(cell.state.rgb)
    for neighs in neighbors.values():
      if len(neighs) == 0:
        in_vector.extend([0]*self.state_vector_length)
      else:
        in_vector.extend([sum(x) for x in zip(*map(lambda cell: cell.state.rgb, neighs))])
    return in_vector

class MLPColorTopologyRule(Rule):
  def __init__(self):
    self.state_vector_length = 3

    self.input_layer_length = self.state_vector_length*5
    self.hidden_layer_length = self.input_layer_length*2
    self.output_layer_length = self.state_vector_length+2 # +2 because we want also growing/dividing states

    self.net = buildNetwork(
        self.input_layer_length,
        self.hidden_layer_length,
        self.output_layer_length)

  def set_weights(self, weights):
    pass

  def get_next_state(self, cell, neighbors):
    in_vector = self.get_input_vector(cell, neighbors)
    out_vector = self.net.activate(in_vector)
    normalized_color_values = self.normalize_to_color(out_vector[:3])
    normalized_topology_values = self.normalize_to_topology(out_vector[-2:])

    new_state = cell.state.create_state()
    new_state.rgb = tuple(normalized_color_values)
    new_state.wants_grow = normalized_topology_values[0]
    new_state.wants_divide = normalized_topology_values[1]
    return new_state

  def normalize_to_color(self, out_vector):
    return map(lambda x: min(255,int(abs(x)*30)),out_vector)

  def normalize_to_topology(self, out_vector):
    return map(lambda x: x > 0, out_vector)

  def get_input_vector(self, cell, neighbors):
    in_vector = []
    in_vector.extend(cell.state.rgb)
    for neighs in neighbors.values():
      if len(neighs) == 0:
        in_vector.extend([0]*self.state_vector_length)
      else:
        in_vector.extend([sum(x) for x in zip(*map(lambda cell: cell.state.rgb, neighs))])
    return in_vector

class ANNColorRule(Rule):
  '''This rule is implementing own neural network that takes chemicals of 
  cells and their internal states as input then calculate one hidden layer
  and then also takes other input and uses this input in activating other 
  neurons in hidden layer. Then outputs cell chemical and state vector.
  '''

  def __init__(self):
    self.chemicals_vector_length = 3
    self.internal_state_vector_length = 3
    self.input_layer_length = 4*self.chemicals_vector_length + self.internal_state_vector_length
    self.hidden_layer_length = self.input_layer_length*2
    self.output_layer_length = self.internal_state_vector_length+self.chemicals_vector_length
    self.randomize_weights()

  def randomize_weights(self):
    number_of_weights = self.total_number_of_weights()
    weights = np.random.rand(number_of_weights)
    self.set_weights(weights)

  def total_number_of_weights(self):
    '''Return total number of weights that are used'''
    return (self.input_layer_length + 1) * self.hidden_layer_length + (self.hidden_layer_length + 1) * self.output_layer_length + self.output_layer_length

  def set_weights(self, new_weights):
    '''Weights we are evolving are passed to neural network by this function.
    list of weight values are sorted like this.

        input -> hidden layer weights = (4*chemical vector + 1*state vector + 1)* hidden layer length
        hidden -> output layer weights = (hidden l. length + 1) * (1*state vector + 1*chemical vector)
        output -> cell color weights = (1*state vector + 1*cemical vector + 1) * 1
        
    So actually we are using 3 types of weights for our network
    '''
    first_slice = (self.input_layer_length + 1) * self.hidden_layer_length
    self.theta1 = np.array(new_weights[:first_slice])
    self.theta1.shape = (self.hidden_layer_length, self.input_layer_length+1)

    second_slice = (self.hidden_layer_length + 1) * self.output_layer_length
    self.theta2 = new_weights[first_slice:first_slice+second_slice]
    self.theta2.shape = (self.output_layer_length, self.hidden_layer_length+1)

    last_slice = self.output_layer_length+1
    self.theta3 = new_weights[-last_slice:]
    self.theta3.shape = (1,self.output_layer_length+1)

  def get_next_state(self, cell, neighbours):
    input_vector = self.get_input_vector(cell, neighbours)
    a1 = np.insert(input_vector, 0, 1)   # insert first bias value
    a2 = np.tanh(np.dot(self.theta1, a1))

    a2 = np.insert(a2,0,1)   # insert first bias value
    out_vector = np.tanh(np.dot(self.theta2, a2))

    new_internal_state = out_vector[:self.internal_state_vector_length]
    new_chemicals = out_vector[-self.chemicals_vector_length:]

    # getting new color is a bit tricky
    additional_chems_vector = np.repeat(.0,self.internal_state_vector_length)
    additional_chems_vector = np.append(additional_chems_vector,cell.state.chemicals)
    out_vector = out_vector + additional_chems_vector
    a3 = np.insert(out_vector, 0, 1)
    new_color = np.dot(self.theta3, a3)/2 + 0.5

    # finally create new state
    new_state = cell.state.create_state()
    new_state.chemicals = cell.state.chemicals + new_chemicals
    new_state.internal = new_internal_state
    new_state.grayscale = int(new_color*255)
    return new_state

  def get_input_vector(self, cell, neighbours):
    ''' Here we are dealing with just one neighbour per direction. It's Square
    Lattice so there is just one neighbour per direction.
    '''
    input_list = []
    input_list.extend(cell.state.internal)
    for direction in ["north", "east", "south", "west"]:
      if len(neighbours[direction]) == 0:
        input_list.extend([.0]*len(cell.state.chemicals))
      else:
        input_list.extend(iter(neighbours[direction]).next().state.chemicals)
    
    if len(input_list) != self.input_layer_length:
      print("{} != {}".format(len(input_list), self.input_layer_length))
      raise Exception("invalid input layer length")
    return np.array(input_list)

