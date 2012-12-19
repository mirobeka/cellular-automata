from cellular_automata.lattices.equiangular_lattice import EquiangularLattice
from cellular_automata.rules.game_of_life_rule import GameOfLifeRule
from cellular_automata.time_step import TimeStep

class GameOfLife:
  def __init__(self, width, height):
    self.lattice = EquiangularLattice(width, height, GameOfLifeRule())

  def getRawData(self):
    return [(cell.x, cell.y, cell.getState(), cell.getSize()) for row in self.lattice.getLattice() for cell in row]

  def setUpInitialConfiguration(self, initialConfiguration):
    map(lambda (state,x,y): self.lattice.initializeStateOfCell(state,x,y), initialConfiguration)

  def nextStep(self, timeStep):
    self.lattice.nextTimeStep(timeStep.getTime())
    timeStep.nextStep()

  def start(self, maxSteps):
    timeStep = TimeStep(maxSteps)
    while timeStep.underMaxSteps():
      self.nextStep(timeStep)
      print("Step #{0:03d}".format(timeStep.getTime()))
      print(self)

  def __str__(self):
    return ''.join([''.join(["{0:02d} ".format(row[0].y)]+[str(cell) for cell in row]) + "|\n" for row in self.lattice.getLattice()])
