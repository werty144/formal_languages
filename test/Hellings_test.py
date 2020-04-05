import tempfile
import unittest
from os import path

from src.Hellings import *

syllabus_graph_triples = ['0 a 1',
                          '1 a 2',
                          '2 a 0',
                          '2 b 3',
                          '3 b 2']

my_bracket_graph_triples = ['0 ( 1',
                            '1 ) 2',
                            '1 ( 3',
                            '3 ) 0',
                            '3 ) 4',
                            '4 ( 3',
                            '4 ) 5']

my_abc_graph_triples = ['0 a 1',
                        '1 b 0',
                        '1 c 2',
                        '1 c 3',
                        '1 b 4',
                        '2 c 2',
                        '2 a 6',
                        '4 c 5',
                        '5 a 3']

syllabus_grammar_rules = ['S A B',
                          'S A S1',
                          'S1 S B',
                          'A a',
                          'B b']


ambiguous_cbs_rules = ['S ( S )',
                       'S S S',
                       'S eps']


deterministic_cbs_rules = ['S ( S ) S',
                           'S eps']


cbs_rules_in_wcnf = ['A0 S A2',
                     'A1 (',
                     'A2 )',
                     'S A1 A0',
                     'S S S',
                     'S eps']


inherently_ambiguous_grammar = ['A a A',
                                'A eps',
                                'C c C',
                                'C eps',
                                'AB a b AB',
                                'AB eps',
                                'BC b c BC',
                                'BC eps',
                                'S AB C',
                                'S A BC',
                                'S eps']

correct_bracket_graph_s_acceptable = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                      ('0', '2'), ('1', '0'), ('1', '4'), ('4', '0'), ('1', '2'), ('4', '2'),
                                      ('0', '5'), ('1', '5'), ('4', '5')]


class TestHellings(unittest.TestCase):
    def test_hellings_on_syllabus_example(self):
        grammar = CFGrammar(syllabus_grammar_rules)
        graph = Graph(syllabus_graph_triples)
        res = hellings(grammar, graph)
        correct = [
            ('A', '0', '1'), ('A', '1', '2'), ('A', '2', '0'), ('B', '2', '3'), ('B', '3', '2'),
            ('S', '1', '3'), ('S1', '1', '2'), ('S', '0', '2'), ('S1', '0', '3'), ('S', '2', '3'),
            ('S1', '2', '2'), ('S', '1', '2'), ('S1', '1', '3'), ('S', '0', '3'), ('S1', '0', '2'),
            ('S', '2', '2'), ('S1', '2', '3')
        ]
        self.assertEqual(correct, res)

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
        correct = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('6', '6'), ('5', '5'), ('1', '2'),
                   ('1', '3'), ('4', '5'), ('0', '1'), ('5', '3'), ('2', '6'), ('0', '5'), ('0', '4'), ('1', '5')]
        self.assertEqual(sorted(correct), sorted(s_acceptable))

    def test_use_hellings_on_syllabus_example(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in syllabus_grammar_rules:
            rf.write(rule + '\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in syllabus_graph_triples:
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
        correct_s_acceptable = ['1 3',
                                '0 2',
                                '2 3',
                                '1 2',
                                '0 3',
                                '2 2']
        self.assertEqual(correct_s_acceptable, my_s_acceptable)

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
