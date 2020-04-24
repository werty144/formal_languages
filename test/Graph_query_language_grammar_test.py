import unittest
import os

from src.CYK import *
from src.CFG import CFGrammar


def get_grammar():
    os.chdir(os.path.dirname(__file__))
    grammar_file = open(os.pardir + '/query_languages/graph_query_language_grammar', 'r')
    rules = grammar_file.read().splitlines()
    grammar_file.close()
    grammar = CFGrammar(rules)
    grammar.start_nonterminal = 'SCRIPT'
    grammar.make_S_start_nonterminal()
    return grammar


class TestGraphQueryGrammar(unittest.TestCase):
    def test_empty(self):
        scritp = ''
        grammar = get_grammar()
        self.assertTrue(cyk(grammar, scritp))

    def test_one_line(self):
        script = 'kw_connect kw_to string semi'
        script = script.split()
        grammar = get_grammar()
        self.assertTrue(cyk(grammar, script))

    def test_syllabus_example(self):
        script = 'kw_connect kw_to string semi\n'\
                 'nt_name op_eq ident nt_name ident nt_name mid lbr rbr semi\n'\
                 'kw_select kw_count lbr ident rbr\n'\
                 'kw_from string\n'\
                 'kw_where lbr ident dot kw_id op_eq int rbr\n' \
                 'op_minus nt_name op_minus op_gr lbr ident rbr semi'
        script = script.split()
        grammar = get_grammar()
        self.assertTrue(cyk(grammar, script))

    def test_lost_semicolon(self):
        script = 'kw_connect kw_to string'
        script = script.split()
        grammar = get_grammar()
        self.assertFalse(cyk(grammar, script))

    def test_my_function(self):
        script = 'kw_write kw_select kw_count_neighbours lbr ident rbr kw_from string\n'\
                 'kw_where lbr ident dot kw_id op_eq int rbr\n' \
                 'op_minus nt_name op_minus op_gr lbr ident rbr\n' \
                 'kw_to string semi'
        script = script.split()
        grammar = get_grammar()
        self.assertTrue(cyk(grammar, script))


if __name__ == '__main__':
    unittest.main()
