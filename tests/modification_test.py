import unittest
from src.parser import *
from src.cfg_modify import *

test_path = "../context_free_grammars/tests/"


class TestParseMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = CFG()
        self.cfg_result = CFG()
        self.A = NonTerminal("A")
        self.B = NonTerminal("B")
        self.C = NonTerminal("C")
        self.D = NonTerminal("D")
        self.S = NonTerminal("S")
        self.a = Terminal("a")
        self.b = Terminal("b")
        self.c = Terminal("c")
        self.d = Terminal("d")

    def _load_cfgs(self, file):
        to_test = test_path + file + ".txt"
        to_check = test_path + file + "_result.txt"
        parse_file_path(self.cfg, to_test)
        parse_file_path(self.cfg_result, to_check)

    def _pretty_print_error(self, msg):
        return "\n" + msg + "\n" + str(self.cfg) + "---------------------\n" + str(self.cfg_result)

    def _compare_cfgs(self):
        self.assertSetEqual(self.cfg.terminals, self.cfg_result.terminals, "terminals")
        self.assertSetEqual(self.cfg.non_terminals, self.cfg_result.non_terminals, "non-terminals")
        self.assertEqual(self.cfg.start_var, self.cfg_result.start_var,
                         self._pretty_print_error("start variable"))
        for key, rules in self.cfg.production_rules.items():
            rules_result = self.cfg_result.production_rules.get(key)
            self.assertTrue(rules_result is not None,
                            self._pretty_print_error("no set for " + str(key) + "in result cfg"))
            self.assertSetEqual(rules, rules_result,
                                self._pretty_print_error("set doesnt match: " + str(key)))

    def test_parse(self):
        parse_file(self.cfg, "erasable_test.txt")
        self.assertSetEqual(self.cfg.non_terminals, {self.A, self.B, self.C, self.S})
        self.assertSetEqual(self.cfg.terminals, {self.a, self.b,
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
        remove_unit_rules(self.cfg)
        print(self.cfg)
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

    def test_nonproductive_removal(self):
        self._load_cfgs("non_productives")
        remove_nonproductive_rules(self.cfg)
        self._compare_cfgs()


if __name__ == '__main__':
    unittest.main()
