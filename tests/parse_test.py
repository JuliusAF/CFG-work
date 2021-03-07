import unittest
from src.parser import *
from src.cfg import CFG


class TestParseMethods(unittest.TestCase):

    def test_file_parse(self):
        cfg = CFG()
        parse_file(cfg, "simple_test.txt")
        self.assertTrue(cfg.start_var == NonTerminal("S"))
        self.assertTrue(NonTerminal("I") in cfg.non_terminals)
        self.assertTrue(Terminal("u") in cfg.terminals)
        print(cfg)

    def test_no_file(self):
        cfg = CFG()
        with self.assertRaises(FileNotFoundError):
            parse_file(cfg, "not_found")


if __name__ == '__main__':
    unittest.main()
