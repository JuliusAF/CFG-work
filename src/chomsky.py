from collections import deque
import itertools

import src.cfg
import src.cfg_modify
import itertools

_chomsky_pref = "_CHOMSKY"
_chomsky_it = 1


def get_chomsky_term(t):
    name = _chomsky_pref + str(t.value)
    return src.cfg.NonTerminal(name)


def add_terminal_rules(cfg):
    for terminal in cfg.terminals:
        cfg.add_rule(src.cfg.Rule(get_chomsky_term(terminal), [terminal]))


def new_rule_name():
    global _chomsky_it
    name = _chomsky_pref + "_RULE" + str(_chomsky_it)
    _chomsky_it += 1
    return name


def split_rule(rule):
    new_rules = []
    old_lhs = rule.lhs
    for i in range(len(rule.rhs) - 2):
        new_non = src.cfg.NonTerminal(new_rule_name())
        new_rules.append(src.cfg.Rule(old_lhs, [rule.rhs[i], new_non]))
        old_lhs = new_non
    else:
        new_rules.append(src.cfg.Rule(old_lhs, [rule.rhs[-2], rule.rhs[-1]]))

    return new_rules


def transform_to_CNF(cfg):
    src.cfg_modify.remove_lambdas(cfg)
    src.cfg_modify.remove_unit_rules(cfg)
    add_terminal_rules(cfg)
    remlist = []
    addlist = []
    for key, rules in cfg.production_rules.items():
        for rule in rules:
            new_rhs = []
            if len(rule.rhs) > 1:
                for var in rule.rhs:
                    if isinstance(var, src.cfg.Terminal):
                        new_rhs.append(get_chomsky_term(var))
                    else:
                        new_rhs.append(var)
                remlist.append(rule)
                addlist.append(src.cfg.Rule(rule.lhs, new_rhs))

    for rem, add in itertools.zip_longest(remlist, addlist):
        cfg.remove_rule(rem)
        cfg.add_rule(add)

    remlist.clear()
    addlist.clear()

    for key, rules in cfg.production_rules.items():
        for rule in rules:
            if len(rule.rhs) > 2:
                addlist += split_rule(rule)
                remlist.append(rule)

    for rem in remlist:
        cfg.remove_rule(rem)

    for add in addlist:
        cfg.add_rule(add)
