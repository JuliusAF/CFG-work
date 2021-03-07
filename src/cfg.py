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

    def duplicate_rule(self, rule, new_lhs):
        new_rule = Rule(new_lhs, rule.rhs)
        existing = self.production_rules.get(new_lhs)
        if existing is None:
            self.production_rules.update({new_lhs: new_rule})
        else:
            existing.add(new_rule)

    def remove_rule(self, rule):
        rules = self.production_rules.get(rule.lhs)
        rules.discard(rule)
        if len(rules) == 0:
            self.production_rules.pop(rule.lhs)

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
                        if isinstance(var, Terminal) or var not in erasable:
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
            if _is_unit_rule(rule):
                unit_rules.add(rule)

    return unit_rules


def _is_unit_rule(rule):
    return len(rule.rhs) == 1 and isinstance(rule.rhs[0], NonTerminal)


def remove_unit_rules(cfg):
    unit_rules = get_unit_rules(cfg)
    for key, rules in cfg.production_rules.items():
        added_rules = {key}
        worklist = []
        for rule in rules:
            if _is_unit_rule(rule) and rule.rhs[0] not in added_rules:
                added_rules.add(rule.rhs[0])
                worklist.append(rule.rhs[0])

        for var in worklist:
            var_rules = cfg.production_rules.get(var)
            if var_rules is None:
                continue

            for rule in var_rules:
                if _is_unit_rule(rule) and rule.rhs[0] not in added_rules:
                    added_rules.add(rule.rhs[0])
                    worklist.append(rule.rhs[0])
                elif not _is_unit_rule(rule):
                    cfg.duplicate_rule(rule, key)

    for rule in unit_rules:
        cfg.remove_rule(rule)


def get_productive_vars(cfg):
    productives = set()
    changed = True
    while changed:
        changed = False
        for key, rules in cfg.production_rules.items():
            for rule in rules:
                productive = True
                for var in rule.rhs:
                    if isinstance(var, NonTerminal) and var not in productives:
                        productive = False
                        break

                if productive and key not in productives:
                    productives.add(key)
                    changed = True
                    break

    return productives


def remove_nonproductive_rules(cfg):
    productives = get_productive_vars(cfg)
    worklist = []
    for key, rules in cfg.production_rules.items():
        for rule in rules:
            for var in rule.rhs:
                if isinstance(var, NonTerminal) and var not in productives:
                    worklist.append(rule)
                    break

    for rem in worklist:
        cfg.remove_rule(rem)
