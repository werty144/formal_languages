import tempfile
import unittest
from os import path

from src.Hellings import *

graph_triples = ['0 a 1',
                 '1 a 2',
                 '2 a 0',
                 '2 b 3',
                 '3 b 2']

grammar_rules = ['S A B',
                 'S A S1',
                 'S1 S B',
                 'A a',
                 'B b']


class TestHellings(unittest.TestCase):
    def test_hellings(self):
        grammar = CFGrammar(grammar_rules)
        graph = Graph(graph_triples)
        res = hellings(grammar, graph)
        correct = [
            ('A', '0', '1'), ('A', '1', '2'), ('A', '2', '0'), ('B', '2', '3'), ('B', '3', '2'),
            ('S', '1', '3'), ('S1', '1', '2'), ('S', '0', '2'), ('S1', '0', '3'), ('S', '2', '3'),
            ('S1', '2', '2'), ('S', '1', '2'), ('S1', '1', '3'), ('S', '0', '3'), ('S1', '0', '2'),
            ('S', '2', '2'), ('S1', '2', '3')
        ]
        self.assertEqual(correct, res)

    def test_use_hellings(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in grammar_rules:
            rf.write(rule + '\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in graph_triples:
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
        res_grammar.sort()
        grammar_rules.sort()
        self.assertEqual(grammar_rules, res_grammar)

        my_s_acceptable = lines[empty_str_ind + 1:]
        correct_s_acceptable = ['1 3',
                                '0 2',
                                '2 3',
                                '1 2',
                                '0 3',
                                '2 2']
        self.assertEqual(correct_s_acceptable, my_s_acceptable)


if __name__ == '__main__':
    unittest.main()
