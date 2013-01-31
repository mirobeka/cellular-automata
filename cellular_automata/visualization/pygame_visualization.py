import pygame, sys
from pygame.locals import *


class PygameVisualization:
  def __init__(self, lattice, fps=30):
    self.lattice = lattice
    self.fps = fps
    self.initPyGame()
    self.initializeBasicColors()

  def initializeBasicColors(self):
    self.black = pygame.Color(0,0,0)
    self.white = pygame.Color(255,255,255)

  def initPyGame(self):
    pygame.init()
    self.fpsClock = pygame.time.Clock()
    self.initWindow()

  def setFPS(self, fps):
    self.fps = fps

  def initWindow(self):
    self.surface = pygame.display.set_mode((self.lattice.width, self.lattice.height))
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
    self.drawLattice(self.lattice.cells)
    self.update()

  def update(self):
    pygame.display.update()
    self.fpsClock.tick(self.fps)

  def clearSurface(self):
    self.surface.fill(self.white)

  def drawLattice(self, cells):
    for cell in cells.values():
      self.drawCell(cell)
    
  def drawCell(self, cell):
    tlx = cell.x - cell.radius
    tly = cell.y - cell.radius
    width = cell.radius*2
    height = cell.radius*2
    rgb = cell.state.rgb
    pyColor = pygame.Color(rgb[0], rgb[1], rgb[2])
    self.drawRect(pyColor,(tlx, tly, width, height))

  def drawRect(self, color, position):
    pygame.draw.rect(self.surface, color, position)

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
