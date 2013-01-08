from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighborhoods import vonNeumannNeighborhood
from cellular_automata.rules.neural_rule import MLPRule

import pygame, sys
from pygame.locals import *

black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)

class App:
  def __init__(self, width, height):
    self.initConstants(width, height)
    self.initCellularAutomata()
    self.initPyGame()

  def initConstants(self, width, height):
    self.fps = 30
    self.resolution = 16
    self.width = width
    self.height = height
    self.latticeDimensions = (width/self.resolution, height/self.resolution)

  def initCellularAutomata(self):
    self.rule = MLPRule()
    # self.rule = AllwaysMergeRule()
    self.lattice = VariableSquareLattice(self.latticeDimensions, vonNeumannNeighborhood, self.rule)

  def initPyGame(self):
    pygame.init()
    self.fpsClock = pygame.time.Clock()
    self.initWindow()

  def initWindow(self):
    self.surface = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Cellular Automata")

  def start(self):
    self.running = True
    self.mainLoop()

  def onEvent(self, event):
    if event.type == QUIT:
      self.quit()
    elif event.type == KEYDOWN:
      self.keyEvent(event)
    elif event.type == MOUSEBUTTONUP:
      self.mouseButtonEvent(event)

  def keyEvent(self, event):
    if event.key == K_ESCAPE:
      pygame.event.post(pygame.event.Event(QUIT))

  def mouseButtonEvent(self, event):
    pass

  def quit(self):
    self.running = False

  def onLoop(self):
    self.lattice.nextStep()
    self.printStats()

  def onRender(self):
    self.clearSurface()
    self.drawLattice()
    self.update()

  def update(self):
    pygame.display.update()
    self.fpsClock.tick(self.fps)

  def clearSurface(self):
    self.surface.fill(white)

  def drawLattice(self):
    map(lambda cell: self.drawCell(cell), self.lattice.cells)
    
  def drawCell(self, cell):
    tlx = cell.x - cell.radius
    tly = cell.y - cell.radius
    width = cell.radius*2
    height = cell.radius*2
    rgb = map(lambda x: int(min(255,abs(30*x))),cell.getState())
    pyColor = pygame.Color(rgb[0], rgb[1], rgb[2])
    pygame.draw.rect(self.surface, pyColor,(tlx, tly, width, height))

  def printStats(self):
    count = len(self.lattice.cells)
    print("time {:05d}".format(pygame.time.get_ticks()))
    print("# Cells : {:03d}".format(count))

  def onCleanup(self):
    print("Ending application loop")
    pygame.quit()
    sys.exit()

  def mainLoop(self):
    while self.running:
      for event in pygame.event.get():
        self.onEvent(event)
      self.onLoop()
      self.onRender()
    self.onCleanup()


if __name__ == "__main__":
  app = App(256,256)
  app.start()

