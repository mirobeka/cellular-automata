from cellular_automata.rules.base import Rule
from random import random


class ReactionRule(Rule):
    '''This rule is reaction part in reaction-diffusion model.
    Diffusion is implemented as part of lattice process while computing next step
    '''

    def get_next_state(self, cell, neighs):
        '''In this reaction rule, we simulate the reaction part of reaction-diffusion
        system
        '''
        return cell.state
