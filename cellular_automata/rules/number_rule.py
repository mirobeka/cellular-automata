from cellular_automata.rules.base import Rule


class NumberRule(Rule):
    def __init__(self, rule_number, number_of_states, threshold):
        self.rules = {}
        self.number_of_states = number_of_states
        self.rule_number = rule_number
        self.threshold = threshold
        self.rules = self.rule_disassembler(rule_number, number_of_states,
                                            threshold, {})

    def rule_disassembler(self, number, base, threshold, rules):
        if number is 0:
            return rules
        rules[self.threshold - threshold] = number % base
        return self.rule_disassembler(number / base, base, threshold - 1, rules)

    def get_next_state(self, cell, neighs):
        sum_of_cell_states = self.get_sum_of_cell_states(cell, neighs)
        if sum_of_cell_states >= self.threshold:
            return self.rules[self.threshold]
        return self.rules[sum_of_cell_states]

