from src.cfg import *
from src.Error import InputError
import re


def parse_file(cfg, file):
    path = "../context_free_grammars/" + file
    with open(path, 'r') as f:
        for line in f:
            parse_rule(cfg, line)


def parse_file_path(cfg, path):
    with open(path, 'r') as f:
        for line in f:
            parse_rule(cfg, line)


def parse_user_input(cfg):
    while True:
        line = input()
        if line == "end":
            return
        else:
            parse_rule(cfg, line)


def parse_rule(cfg, rule):
    split = rule.strip().replace(" ", "").split("->")
    if len(split) != 2:
        raise InputError(rule, "Rule is not separated by a single arrow: '->'")

    lhs = split[0]
    rhs = split[1].split("|")

    if not re.match(r"[A-Z][0-9]*", lhs):
        raise InputError(lhs, "LHS does not match specified rule format")

    for r in rhs:
        split_rule = []
        temp = None

        for c in r:
            if not c.isnumeric() and temp is not None:
                split_rule.append(NonTerminal(temp))
                temp = None

            if c.islower():
                split_rule.append(Terminal(c))
            elif c.isupper():
                temp = c
            elif c.isnumeric():
                if temp is None:
                    raise InputError(r, "Number does not follow a non terminal: " + c)
                else:
                    temp += c
            elif c == "&":
                if len(split_rule) != 0 and len(r) != 1:
                    raise InputError(r, "Lambda must exist by itself in a rule")
                else:
                    split_rule.append(Lambda())
            else:
                raise InputError(r, "Unknown character encountered: " + c)
        else:
            if temp is not None:
                split_rule.append(NonTerminal(temp))

        new_rule = Rule(NonTerminal(lhs), split_rule)
        cfg.add_rule(new_rule)
