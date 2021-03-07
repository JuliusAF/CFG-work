from src.cfg import *


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
