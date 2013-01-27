from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.rules.neural_rule import MLPRule

class Objective(object):
  '''This is just abstract class to be extended. Extend this class for your
  objective that should be optimized.
  '''
  def __init__(self):
    pass

  @staticmethod
  def error_function(pattern, lattice):
    ''' error funtion compare given latice with desired pattern and returns
    scalar value describing difference between those 2 lattices
    
    This method should be implemented to reflect objective that should be
    optimized.

    For example, if I want to optimized structure and topology of cellular
    automata(CA), in this function should be compared resulting lattice and defined
    pattern and thid comparison reflected by scalar value.

    In other case, I we want to optimise structure and also states of CA se should
    compare states and structure and then sum this error and return scalar value
    '''
    raise NotImplementedError("error function not implemented")

  def objective_function(self, vector):
    ''' objective funtion is main function that is minimized by cma-es algorithm
    In our case, we are optimizing weights of neural network, but we can optimize
    anything we want.

    On the input of objective_function is optimized vector of values.
    On the output of objective_function must be scalar value that is minimized.
    
    This method should be implemented in a way that suits your optimalization
    needs.'''
    raise NotImplementedError("method objective_function not implemented")

class TwoBandObjective(Objective):
  def __init__(self):
    Objective.__init__(self)
    self.initialize_experiment_parameters()

  def initialize_experiment_parameters(self):
    yaml_configuration = self.load_lattice_configuration("data/two_band_configuration.ltc")
    self.desired_lattice = SquareLattice.loadFromFile(yaml_configuration)
    self.dimensions = (self.desired_lattice.width, self.desired_lattice.height)
    self.stop_criterion = CAStopCriterion()

  def load_lattice_configuration(self, file_name):
    try:
      data = open(file_name, 'r')
    except IOError as e:
      print("error while openning file \"{}\"".format(file_name))
      print(e)
      return None
    else:
      configuration = yaml.load(data)
      data.close()

    return configuration
  
  @staticmethod
  def error_function(pattern, lattice):
    '''check desired pattern with given lattice. Return sum of state differences'''
    return sum([self.difference(pattern.cells[key], lattice.cells[key]) for key in pattern.cells.keys()])

  @staticmethod
  def difference(cell1, cell2):
    return sum(map(lambda (x,y): abs(x-y), zip(cell1.state, cell2.state)))

  def objective_function(self, weights):
    '''Constructs cellular automata, set weights of MLP as rule for cellular
    automata, run cellular automata until it stops and compare result with
    desired pattern. In this case desired pattern is two band.'''
    rule = MLPRule()
    rule.set_weights(weights)
    lattice = SquareLattice.create_initialized(rule)
    lattice.run(self.stop_criterion)
    return self.error_function(self.desired_lattice, lattice)

class CircleObjective(Objective):
  pass    # TODO

class CAStopCriterion(object):
  '''This is base class of cellular automata stop criterion.
  class should be extended to check more that just number of steps as stopping
  criterion.'''

  def should_run(self, lattice):
    '''Return True/False if Cellular Automata should run/stop'''
    return self.time < 1000:

