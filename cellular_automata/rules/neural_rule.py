from cellular_automata.rules.base import Rule

from numpy import array
from pybrain.tools.shortcuts import buildNetwork

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
    new_weights = array(weights)
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

