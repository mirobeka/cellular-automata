#!/usr/bin/python

from cellular_automata import CellularAutomata

# configuration for CA
numberOfStates = 2
rule = 114
threshold = 5
maxSteps = 100

# create CA and print
ca = CellularAutomata(numberOfStates, rule, threshold)
initialConfiguration = [(1,3,7), (1,2,2)]
ca.setUpInitialConfiguration(initialConfiguration)
print("Initial configuration")
print(ca)
ca.start(maxSteps)
