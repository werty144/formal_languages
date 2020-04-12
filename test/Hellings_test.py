import tempfile
import unittest
from os import path

from Grammars_n_graphs import *
from src.Hellings import *


class TestHellings(unittest.TestCase):
    def test_hellings_on_syllabus_example(self):
        grammar = CFGrammar(syllabus_grammar_rules)
        graph = Graph(syllabus_graph_triples1)
        res = hellings(grammar, graph)
        self.assertEqual(correct_syllabus_hellings_answer, res)

    def test_hellings_on_my_bracket_graph_on_ambiguous_grammar(self):
        grammar = CFGrammar(ambiguous_cbs_rules)
        graph = Graph(my_bracket_graph_triples)
        res = hellings(grammar, graph)
        s_acceptable = [(u, v) for nonterminal, u, v in res if nonterminal == 'S']

        self.assertEqual(sorted(correct_bracket_graph_s_acceptable), sorted(s_acceptable))

    def test_hellings_on_my_bracket_graph_on_deterministic_grammar(self):
        grammar = CFGrammar(deterministic_cbs_rules)
        graph = Graph(my_bracket_graph_triples)
        res = hellings(grammar, graph)
        s_acceptable = [(u, v) for nonterminal, u, v in res if nonterminal == 'S']
        self.assertEqual(sorted(correct_bracket_graph_s_acceptable), sorted(s_acceptable))

    def test_hellings_on_my_abc_graph_on_inherently_ambiguous_grammar(self):
        grammar = CFGrammar(inherently_ambiguous_grammar)
        graph = Graph(my_abc_graph_triples)
        res = hellings(grammar, graph)
        s_acceptable = [(u, v) for nonterminal, u, v in res if nonterminal == 'S']
        self.assertEqual(sorted(correct_s_acceptable_abc_graph), sorted(s_acceptable))

    def test_use_hellings_on_syllabus_example(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in syllabus_grammar_rules:
            rf.write(rule + '\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in syllabus_graph_triples1:
            gf.write(triple + '\n')
        gf.close()
        res_file = path.join(self.test_dir, 'res.txt')
        use_hellings(grammar_file, graph_file, res_file)
        rf = open(res_file, 'r')
        lines = rf.read().splitlines()
        rf.close()
        try:
            empty_str_ind = lines.index('')
        except ValueError:
            self.fail()
        res_grammar = lines[:empty_str_ind]
        self.assertEqual(sorted(syllabus_grammar_rules), sorted(res_grammar))

        my_s_acceptable = lines[empty_str_ind + 1:]
        self.assertEqual(correct_syllabus_s_acceptable, my_s_acceptable)

    def test_use_hellings_on_my_bracket_graph_example(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in ambiguous_cbs_rules:
            rf.write(rule + '\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in my_bracket_graph_triples:
            gf.write(triple + '\n')
        gf.close()
        res_file = path.join(self.test_dir, 'res.txt')
        use_hellings(grammar_file, graph_file, res_file)
        rf = open(res_file, 'r')
        lines = rf.read().splitlines()
        rf.close()
        try:
            empty_str_ind = lines.index('')
        except ValueError:
            self.fail()
        res_grammar = lines[:empty_str_ind]
        self.assertEqual(sorted(cbs_rules_in_wcnf), sorted(res_grammar))
        my_s_acceptable = lines[empty_str_ind + 1:]
        correct_s_acceptable = [u + ' ' + v for u, v in correct_bracket_graph_s_acceptable]
        self.assertEqual(sorted(correct_s_acceptable), sorted(my_s_acceptable))


if __name__ == '__main__':
    unittest.main()
