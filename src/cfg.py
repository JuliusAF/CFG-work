import copy


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

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def get_rhs_string(self):
        ret = ""
        for var in self.rhs:
            ret += str(var)
        return ret

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Rule) and str(other) == str(self)

    def __str__(self):
        return str(self.lhs) + " -> " + Rule.get_rhs_string(self)

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
        self._refs = dict()
        self.production_rules = dict()
        self.start_var = None

    def _add_refs(self, rule):
        if rule.rhs[0] == Lambda():
            return

        for var in rule.rhs:
            var_refs = self._refs.get(var)
            if var_refs is None:
                self._refs.update({var: {rule}})
            else:
                var_refs.add(rule)

    def _remove_refs(self, rule):
        if rule.rhs[0] == Lambda():
            return

        for var in rule.rhs:
            var_refs = self._refs.get(var)
            if var_refs is not None:
                var_refs.discard(rule)
                if len(var_refs) == 0:
                    self._refs.pop(var)
                    if isinstance(var, Terminal):
                        self.terminals.discard(var)
                    elif isinstance(var, NonTerminal) and self.production_rules.get(var) is None:
                        self.non_terminals.discard(var)

    def add_rule(self, rule):
        if len(self.production_rules) == 0:
            self.start_var = rule.lhs

        existing = self.production_rules.get(rule.lhs)
        if existing is None:
            self.production_rules.update({rule.lhs: {rule}})
        else:
            existing.add(rule)

        self.non_terminals.add(rule.lhs)
        if not isinstance(rule.rhs[0], Lambda):
            for var in rule.rhs:
                if isinstance(var, Terminal):
                    self.terminals.add(var)
                elif isinstance(var, NonTerminal):
                    self.non_terminals.add(var)
        self._add_refs(rule)

    def duplicate_rule(self, rule, new_lhs):
        new_rule = Rule(new_lhs, rule.rhs)
        existing = self.production_rules.get(new_lhs)
        if existing is None:
            self.production_rules.update({new_lhs: new_rule})
        else:
            existing.add(new_rule)
        self.non_terminals.add(new_lhs)
        self._add_refs(new_rule)

    def remove_rule(self, rule):
        rules = self.production_rules.get(rule.lhs)
        rules.discard(rule)
        if len(rules) == 0:
            self.production_rules.pop(rule.lhs)
        self._remove_refs(rule)

    def __str__(self):
        ret = "Non-Terminals: " + str(self.non_terminals) + "\n" + \
              "Terminals: " + str(self.terminals) + "\n" + \
              "Production rules:\n"

        for terminal, rules in self.production_rules.items():
            ret += str(terminal) + " -> "
            count = 0

            for rule in rules:
                count += 1
                ret += rule.get_rhs_string()
                if count is not len(rules):
                    ret += " | "

            ret += "\n"

        ret += "Starting symbol: " + str(self.start_var) + "\n"
        return ret