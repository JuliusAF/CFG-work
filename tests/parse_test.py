import unittest
from src.parser import *
from src.cfg import CFG
import src.CYK_parser


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

    def _load_cfg(self, name):
        path = test_path + name + ".txt"
        parse_file_path(self.cfg, path)

    def test_file_parse(self):
        cfg = CFG()
        parse_file(cfg, "simple_test.txt")
        self.assertTrue(cfg.start_var == NonTerminal("S"))
        self.assertTrue(NonTerminal("I") in cfg.non_terminals)
        self.assertTrue(Terminal("u") in cfg.terminals)

    def test_no_file(self):
        cfg = CFG()
        with self.assertRaises(FileNotFoundError):
            parse_file(cfg, "not_found")

    def test_cyk_parser(self):
        self._load_cfg("cyk_parser_simple")
        word = [self.a, self.b, self.b, self.b]
        self.assertTrue(src.CYK_parser.cyk_parser(self.cfg, word))

    def test_cyk_parser1(self):
        self._load_cfg("cyk_parser_simple1")
        word = [self.a, self.c, self.a, self.c]
        self.assertFalse(src.CYK_parser.cyk_parser(self.cfg, word))

    def test_cyk_parser1_1(self):
        self._load_cfg("cyk_parser_simple1")
        word = [self.a, self.c, self.a, self.c, self.c]
        self.assertTrue(src.CYK_parser.cyk_parser(self.cfg, word))


if __name__ == '__main__':
    unittest.main()
