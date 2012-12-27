from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.rules.game_of_life_rule import GameOfLifeRule
from cellular_automata.time_step import TimeStep

class GameOfLife:
  def __init__(self, width, height):
    self.lattice = SquareLattice(width, height, GameOfLifeRule())

  def setUpInitialConfiguration(self, initialConfiguration):
    map(lambda (state,x,y): self.lattice.setStateOfCell(state,x,y), initialConfiguration)

  def start(self, maxSteps):
    step = 0
    while step < maxSteps:
      step += 1
      self.lattice.nextStep()
      print("Step #{0:03d}".format(step))
      print(self)

  def __str__(self):
    return ''.join([''.join(["{0:02d} ".format(row[0].y)]+[str(cell) for cell in row]) + "|\n" for row in self.lattice.getLattice()])
