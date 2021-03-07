import unittest
from src.parser import *
from src.cfg import CFG, get_erasable_vars, remove_lambdas


class TestParseMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = CFG()
        self.A = Terminal("A")
        self.B = Terminal("B")
        self.C = Terminal("C")
        self.D = Terminal("D")
        self.S = Terminal("S")
        self.a = NonTerminal("a")
        self.b = NonTerminal("b")
        self.c = NonTerminal("c")
        self.d = NonTerminal("d")

    def test_parse(self):
        parse_file(self.cfg, "erasable_test.txt")
        self.assertSetEqual(self.cfg.terminals, {self.A, self.B, self.C, self.S})
        self.assertSetEqual(self.cfg.non_terminals, {self.a, self.b,
                                                     self.c, self.d})

    def test_erasable(self):
        parse_file(self.cfg, "erasable_test.txt")
        erasables = get_erasable_vars(self.cfg)
        self.assertSetEqual(erasables, {self.A, self.B, self.C})

    def test_lambda_removal(self):
        parse_file(self.cfg, "lambda_removal.txt")
        remove_lambdas(self.cfg)
        # check if S rules have been expanded
        s_rules = {Rule(self.S, [self.A, self.B, self.a, self.C]),
                   Rule(self.S, [self.B, self.a, self.C]),
                   Rule(self.S, [self.A, self.a, self.C]),
                   Rule(self.S, [self.A, self.B, self.a]),
                   Rule(self.S, [self.A, self.a]),
                   Rule(self.S, [self.B, self.a]),
                   Rule(self.S, [self.a]),
                   Rule(self.S, [self.a, self.C])}
        self.assertSetEqual(self.cfg.production_rules.get(self.S), s_rules)
        # check there are no more lambda rules
        for key, rules in self.cfg.production_rules.items():
            self.assertFalse(Rule(key, [Lambda()]) in rules)

    def test_unit_rule_removal(self):
        parse_file(self.cfg, "unit_rule_removal.txt")
        s_rules = {Rule(self.S, [self.a]),
                   Rule(self.S, [self.b, self.b]),
                   Rule(self.S, [self.b, self.c]),
                   Rule(self.S, [self.A, self.a])}
        a_rules = {Rule(self.A, [self.a]),
                   Rule(self.A, [self.b, self.c]),
                   Rule(self.A, [self.b, self.b])}
        b_rules = {Rule(self.B, [self.a]),
                   Rule(self.B, [self.b, self.c]),
                   Rule(self.B, [self.b, self.b])}
        self.assertSetEqual(self.cfg.production_rules.get(self.S), s_rules)
        self.assertSetEqual(self.cfg.production_rules.get(self.A), a_rules)
        self.assertSetEqual(self.cfg.production_rules.get(self.B), b_rules)


if __name__ == '__main__':
    unittest.main()
