from cellular_automata.rules.base import Rule

class NumberRule(Rule):
  def __init__(self, ruleNumber, numberOfStates, threshold):
    self.rules = {}
    self.numberOfStates = numberOfStates
    self.ruleNumber = ruleNumber
    self.threshold = threshold
    self.rules = self.ruleDisassembler(ruleNumber, numberOfStates, threshold, {})

  def ruleDisassembler(self, number, base, threshold, rules):
    if number is 0:
      return rules
    rules[self.threshold - threshold] = number % base
    return self.ruleDisassembler(number / base, base, threshold-1, rules)

  def get_next_state(self, cell, neighs):
    sum_of_cell_states = self.get_sum_of_cell_states(cell, neighs)
    if sum_of_cell_states >= self.threshold:
      return self.rules[self.threshold]
    return self.rules[sum_of_cell_states]

