class Terminal:
    def __init__(self, t):
        self.value = t

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, Terminal) and other.value == self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class NonTerminal:
    def __init__(self, n):
        self.value = n

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, NonTerminal) and other.value == self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class Lambda:
    def __init__(self):
        pass

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, Lambda)

    def __str__(self):
        return "lambda"

    def __repr__(self):
        return str(self)


class Rule:
    """
    Class to encapsulate rules

    lhs = Terminal symbol on lhs
    rhs = string of lhs replacement rule
    rhs_split = tokens of type Terminal, NonTerminal, Lambda for replacement rule
    """

    def __init__(self, lhs, rhs, rhs_split):
        self.lhs = lhs
        self.rhs = rhs
        self.rhs_split = rhs_split

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Rule) and str(other) == str(self)

    def __str__(self):
        return str(self.lhs) + ": " + str(self.rhs)

    def __repr__(self):
        return str(self)


class CFG:
    """
    Class to encapsulate a context free grammar

    terminals = a set of terminals of type Terminal
    non_terminals = a set of non-terminals of type NonTerminal
    production_rules = a mapping of Terminal to a set of production rules
    start_var = the starting symbol of the CFG

    """

    def __init__(self):
        self.terminals = set()
        self.non_terminals = set()
        self.production_rules = {}
        self.start_var = None

    def add_rule(self, rule):
        if len(self.production_rules) == 0:
            self.start_var = rule.lhs

        existing = self.production_rules.get(rule.lhs)
        if existing is None:
            existing = {rule}
        else:
            existing.add(rule)

        if not isinstance(rule.rhs_split[0], Lambda):
            self.terminals.add(rule.lhs)
            for var in rule.rhs_split:
                if isinstance(var, Terminal):
                    self.terminals.add(var)
                elif isinstance(var, NonTerminal):
                    self.non_terminals.add(var)

        self.production_rules.update({rule.lhs: existing})

    def __str__(self):
        ret = "Terminals: " + str(self.terminals) + "\n" + \
              "Non-terminals: " + str(self.non_terminals) + "\n" + \
              "Production rules:\n"

        for terminal, rules in self.production_rules.items():
            ret += str(terminal) + " -> "
            count = 0

            for rule in rules:
                count += 1
                ret += rule.rhs
                if count is not len(rules):
                    ret += " | "

            ret += "\n"

        ret += "Starting symbol: " + str(self.start_var) + "\n"
        return ret
