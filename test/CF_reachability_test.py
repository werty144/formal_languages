import tempfile
import unittest
from os import path
from src.CF_reachability import *

from Grammars_n_graphs import *

formated_rools = [(r.split()[0], r.split()[1:]) for r in syllabus_grammar_rules]

m1 = np.array([[Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['A']),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['B'])],

               [Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, ['A']), Nonterminal_set(formated_rools, [])],

               [Nonterminal_set(formated_rools, ['A']), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])],

               [Nonterminal_set(formated_rools, ['B']), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])]]
              )

m2 = np.array([[Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])],

               [Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])],

               [Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['S'])],

               [Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])]]
              )

m3 = np.array([[Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['A']),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['B'])],

               [Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, ['A']), Nonterminal_set(formated_rools, [])],

               [Nonterminal_set(formated_rools, ['A']), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, ['S'])],

               [Nonterminal_set(formated_rools, ['B']), Nonterminal_set(formated_rools, []),
                Nonterminal_set(formated_rools, []), Nonterminal_set(formated_rools, [])]]
              )

syllabus_example_answer = [[['S1', 'S'], ['A'], [], ['B', 'S1', 'S']],
                           [['S1', 'S'], [], ['A'], ['S1', 'S']],
                           [['A', 'S1', 'S'], [], [], ['S1', 'S']],
                           [['B'], [], [], []]]


class TestCF_reachability(unittest.TestCase):
    def test_matrix_addition(self):
        self.assertTrue(np.array_equal(m1 + m2, m3))

    def test_matrix_multiplication(self):
        self.assertTrue(np.array_equal(np.dot(m1, m1), m2))

    def test_reachability_using_matrix(self):
        graph = Graph(syllabus_graph_triples2)
        grammar = CFGrammar(syllabus_grammar_rules)
        res = reachability_using_matrix(grammar, graph)
        self.assertEqual(len(res), len(syllabus_example_answer))
        for i in range(len(res)):
            self.assertEqual(len(res[i]), len(syllabus_example_answer[i]))
            for j in range(len(res[i])):
                self.assertEqual(sorted(res[i][j]), sorted(syllabus_example_answer[i][j]))

    def test_use_reachability_using_matrix(self):
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
        use_reachability_using_matrix(grammar_file, graph_file, res_file)
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
        self.assertEqual(sorted(correct_syllabus_s_acceptable), sorted(my_s_acceptable))

    def test_use_reachability_using_matrix_on_my_bracket_graph_example(self):
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
        use_reachability_using_matrix(grammar_file, graph_file, res_file)
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
        correct_s_acceptable = [str(u) + ' ' + str(v) for u, v in correct_bracket_graph_s_acceptable]
        self.assertEqual(sorted(correct_s_acceptable), sorted(my_s_acceptable))


if __name__ == '__main__':
    unittest.main()
