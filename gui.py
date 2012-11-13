#!/usr/bin/python
import pygame, sys
from pygame.locals import *
from cellular_automata import CellularAutomata
from cellular_automata import TimeStep

# pygame configuration
windowTitle = "Cellular Automata"
width = 800
height = 800

# initialize pygame
pygame.init()
fpsClock = pygame.time.Clock()
windowSurfaceObject = pygame.display.set_mode((width, height))
pygame.display.set_caption(windowTitle)

# CA configuration
numberOfStates = 2
rule = 106
threshold = 5
maxSteps = 1000

# initialize Cellular Automata
ca = CellularAutomata(numberOfStates, rule, threshold)
initialConfiguration = [(1,3,7), (1,2,2)]
ca.setUpInitialConfiguration(initialConfiguration)

# set up ca timeStep for CA
timeStep = TimeStep(maxSteps)

# some colors
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)


# dirty dirty solution
rectSize = width / 50

def drawCell(x, y, state, size):
  cellColor = blackColor if state else whiteColor
  pygame.draw.rect(windowSurfaceObject, cellColor, (x*rectSize,y*rectSize,rectSize,rectSize))

while timeStep.underMaxSteps():
  windowSurfaceObject.fill(pygame.Color(255,255,255))
  # draw CAs cells
  map(lambda (x,y,state,size): drawCell(x,y,state, size), ca.getRawData())

  ca.nextStep(timeStep)

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  pygame.display.update()
  fpsClock.tick(30)

