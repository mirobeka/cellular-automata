#!/usr/bin/python
from cellular_automata.game_of_life import GameOfLife

# configuration for CA
maxSteps = 390

# glider gun initial configuration
gliderGun = [
    (1,24,2), (1,22,3), (1,24,3), (1,12,4), (1,13,4),
    (1,20,4), (1,21,4), (1,34,4), (1,35,4), (1,11,5),
    (1,15,5), (1,20,5), (1,21,5), (1,34,5), (1,35,5),
    (1,0,6),  (1,1,6),  (1,10,6), (1,16,6), (1,20,6),
    (1,21,6), (1,0,7),  (1,1,7),  (1,10,7), (1,14,7),
    (1,16,7), (1,17,7), (1,22,7), (1,24,7), (1,10,8),
    (1,16,8), (1,24,8), (1,11,9), (1,15,9), (1,12,10),
    (1,13,10)
]

# create CA and print
game = GameOfLife(40, 34)
game.setUpInitialConfiguration(gliderGun)

# start game
game.start(maxSteps)
