from rule import Rule

class NumberRule(Rule):
  def __init__(self, ruleNumber, numberOfStates, threshold):
    self.rules = {}
    self.numberOfStates = numberOfStates
    self.ruleNumber = ruleNumber
    self.threshold = threshold
    self.rules = self.ruleDisassembler(ruleNumber, numberOfStates, threshold, {})

  def __str__(self):
    return ''.join([str(key) + " => " + str(value) + "\n" for key, value in self.rules.items()])

  def ruleDisassembler(self, number, base, threshold, rules):
    if number is 0:
      return rules
    rules[self.threshold - threshold] = number % base
    return self.ruleDisassembler(number / base, base, threshold-1, rules)

  def getNextState(self, sumOfCellStates):
    if sumOfCellStates >= self.threshold:
      return self.rules[self.threshold]
    return self.rules[sumOfCellStates]

