import unittest
from src.parser import *
from src.cfg import CFG


class TestParseMethods(unittest.TestCase):

    def test_file_parse(self):
        cfg = CFG()
        parse_file(cfg, "simple_test.txt")
        self.assertTrue(cfg.start_var == Terminal("S"))
        self.assertTrue(Terminal("I") in cfg.terminals)
        self.assertTrue(NonTerminal("u") in cfg.non_terminals)

    def test_no_file(self):
        cfg = CFG()
        with self.assertRaises(FileNotFoundError):
            parse_file(cfg, "not_found")


if __name__ == '__main__':
    unittest.main()
