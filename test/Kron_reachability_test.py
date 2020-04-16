import tempfile
import unittest
from os import path
from src.PDA import *
from Grammars_n_graphs import *
from src.CFG import CFGrammar


class TestKronReachability(unittest.TestCase):
    def test_reachability_using_kron_on_syllabus_example1(self):
        syllabus_pda_graph = make_syllabus_pda_graph1()
        syllabus_graph = make_syllabus_graph1()
        get_nonterminals = {0: 'S', 1: 'S', 2: 'S', 3: 'S'}
        grammar = CFGrammar(['S A B', 'S A S B', 'A a', 'B b'])
        res_graph = reachability_using_kron(syllabus_pda_graph, syllabus_graph, get_nonterminals, grammar)
        correct_edges = [(0, 1, ['a']), (0, 2, ['S']), (0, 3, ['S']), (1, 2, ['a', 'S']), (1, 3, ['S']), (2, 0, ['a']),
                         (2, 3, ['b', 'S']), (2, 2, ['S']), (3, 2, ['b'])]
        self.assertEqual(sorted(correct_edges), sorted(res_graph.edges(data='label')))

    def test_reachability_using_kron_on_syllabus_example2(self):
        syllabus_pda_graph = make_syllabus_pda_graph2()
        syllabus_graph = make_syllabus_graph2()
        grammar = CFGrammar(['S a S b S', 'S eps'])
        get_nonterminals = {0: 'S', 1: 'S', 2: 'S', 3: 'S', 4: 'S'}
        res_graph = reachability_using_kron(syllabus_pda_graph, syllabus_graph, get_nonterminals, grammar)
        correct_edges = [(0, 1, ['a']), (0, 0, ['S']), (0, 2, ['S']), (0, 4, ['S']), (0, 6, ['S']), (1, 2, ['b']),
                         (1, 1, ['S']), (2, 3, ['a']), (2, 2, ['S']), (2, 4, ['S']), (2, 6, ['S']), (3, 4, ['b']),
                         (3, 3, ['S']), (4, 5, ['a']), (4, 4, ['S']), (4, 6, ['S']), (5, 6, ['b']), (5, 5, ['S']),
                         (6, 6, ['S'])]
        self.assertEqual(sorted(correct_edges), sorted(res_graph.edges(data='label')))

    def test_using_reachability_using_kron_on_syllabus_example1_simple_input(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        rf.write('S a b\n')
        rf.write('S a S b\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in syllabus_graph_triples1:
            gf.write(triple + '\n')
        gf.close()
        res_file = path.join(self.test_dir, 'res.txt')
        use_reachability_using_kron(grammar_file, graph_file, res_file)

        rf = open(res_file, 'r')
        lines = rf.read().splitlines()
        rf.close()
        try:
            empty_str_ind = lines.index('')
        except ValueError:
            self.fail()

        res_matrix = lines[:empty_str_ind]
        correct_matrix = ["..['a']....",
                          '.......',
                          ".['b'].....",
                          ".....['a'].",
                          '.......',
                          "......['S']",
                          "....['b'].."]
        self.assertEqual(res_matrix, correct_matrix)

        my_s_acceptable = lines[empty_str_ind + 1:]
        self.assertEqual(sorted(correct_syllabus_s_acceptable), sorted(my_s_acceptable))

    def test_using_reachability_using_kron_on_syllabus_example1_hard_input(self):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        rf.write('S a b | a S b\n')
        rf.close()
        graph_file = path.join(self.test_dir, 'graph.txt')
        gf = open(graph_file, 'w')
        for triple in syllabus_graph_triples1:
            gf.write(triple + '\n')
        gf.close()
        res_file = path.join(self.test_dir, 'res.txt')
        use_reachability_using_kron(grammar_file, graph_file, res_file)

        rf = open(res_file, 'r')
        lines = rf.read().splitlines()
        rf.close()
        try:
            empty_str_ind = lines.index('')
        except ValueError:
            self.fail()

        res_matrix = lines[:empty_str_ind]
        correct_matrix = ["...['a']",
                          "..['b'].",
                          '....',
                          ".['S']['b']."]
        self.assertEqual(res_matrix, correct_matrix)

        my_s_acceptable = lines[empty_str_ind + 1:]
        self.assertEqual(sorted(correct_syllabus_s_acceptable), sorted(my_s_acceptable))


if __name__ == '__main__':
    unittest.main()
