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

        if not isinstance(rule.rhs[0], Lambda):
            self.terminals.add(rule.lhs)
            for var in rule.rhs:
                if isinstance(var, Terminal):
                    self.terminals.add(var)
                elif isinstance(var, NonTerminal):
                    self.non_terminals.add(var)

        self.production_rules.update({rule.lhs: existing})

    def remove_rule(self, rule):
        rules = self.production_rules.get(rule.lhs)
        rules.discard(rule)

    def __str__(self):
        ret = "Terminals: " + str(self.terminals) + "\n" + \
              "Non-terminals: " + str(self.non_terminals) + "\n" + \
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


def get_erasable_vars(cfg):
    erasable = set()

    changed = True
    while changed:
        changed = False
        for key, rules in cfg.production_rules.items():
            if key in erasable:
                continue

            for rule in rules:
                if isinstance(rule.rhs[0], Lambda):
                    erasable.add(key)
                    changed = True
                else:
                    can_erase = True
                    for var in rule.rhs:
                        if isinstance(var, NonTerminal) or var not in erasable:
                            can_erase = False
                            break
                    if can_erase:
                        erasable.add(key)
                        changed = True

    return erasable


# for every erasable variable in a rule, it adds a copy of the rule
# sans the erasable variable to 'to_add'
def _remove_lambdas_help(erasable, to_add, rule):
    for i in range(len(rule.rhs)):
        if rule.rhs[i] in erasable:
            temp = copy.deepcopy(rule.rhs)
            temp.pop(i)
            to_add.append(Rule(rule.lhs, temp))


# remove all lambda production rules
def remove_lambdas(cfg):
    erasable = get_erasable_vars(cfg)
    for key, rules in cfg.production_rules.items():
        to_add = []
        count = 0
        for rule in rules:
            _remove_lambdas_help(erasable, to_add, rule)

            while count < len(to_add):
                _remove_lambdas_help(erasable, to_add, to_add[count])
                count += 1

        cfg.production_rules.update({key: rules.union(set(to_add))})

    for erase in erasable:
        cfg.remove_rule(Rule(erase, [Lambda()]))


# returns a set of all unit production rules
def get_unit_rules(cfg):
    unit_rules = set()
    for keys, rules in cfg.production_rules.items():
        for rule in rules:
            if len(rule.rhs) == 1 and rule.rhs[0] in cfg.terminals:
                unit_rules.add(rule)

    return unit_rules


def remove_unit_rules(cfg):
    unit_rules = get_unit_rules(cfg)
