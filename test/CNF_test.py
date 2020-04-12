import unittest
import tempfile
from os import path
from src.CFG import *

rules = ['S a X b X',
         'S a Z',
         'X a Y',
         'X b Y',
         'X eps',
         'Y X',
         'Y c c',
         'Z Z X']

cbs_rules = ['S a S b S',
             'S eps']


class TestCNF(unittest.TestCase):
    def test_get_rid_of_long_rules(self):
        my_grammar = CFGrammar(rules)
        my_grammar.get_rid_of_long_rules()
        for _, expr in my_grammar.rules:
            self.assertLessEqual(len(expr), 2)

    def test_get_epsilon_producing_nonterminals(self):
        my_grammar = CFGrammar(rules)
        eps_producing_nonterminals = my_grammar.get_eps_producing_nonterminals()
        eps_producing_nonterminals.sort()
        self.assertEqual(eps_producing_nonterminals, ['X', 'Y'])

    def test_get_rid_of_eps_rules(self):
        my_grammar = CFGrammar(rules)
        my_grammar.get_rid_of_eps_rules()
        cnt = 0
        for nonterminal, expr in my_grammar.rules:
            if expr == 'eps':
                self.assertEqual(nonterminal, my_grammar.start_nonterminal)
                cnt += 1
        self.assertLessEqual(cnt, 1)

    def test_get_rid_of_chain_rules(self):
        my_grammar = CFGrammar(rules)
        my_grammar.get_rid_of_chain_rules()
        for nonterminal, expr in my_grammar.rules:
            if len(expr) == 1:
                self.assertTrue(expr[0] in my_grammar.terminals)

    def test_get_rid_of_useless_symbols(self):
        my_grammar = CFGrammar(rules)
        my_grammar.get_rid_of_long_rules()
        my_grammar.get_rid_of_useless_symbols()
        self.assertFalse('Z' in my_grammar.nonterminals)
        for nonterminal, expr in my_grammar.rules:
            self.assertNotEqual('Z', nonterminal)
            self.assertFalse('Z' in expr)

    def test_make_lonely_terminals(self):
        my_grammar = CFGrammar(rules)
        my_grammar.get_rid_of_long_rules()
        my_grammar.make_lonely_terminals()
        for nonterminal, expr in my_grammar.rules:
            if len(expr) == 2:
                self.assertTrue(expr[0] in my_grammar.nonterminals and expr[1] in my_grammar.nonterminals)

    def test_to_cnf(self):
        my_grammar = CFGrammar(rules)
        my_grammar.to_cnf()
        for nonterminal, expr in my_grammar.rules:
            self.assertLessEqual(len(expr), 2)
            if len(expr) == 1:
                self.assertTrue(expr[0] in my_grammar.terminals)
            if len(expr) == 2:
                self.assertTrue(expr[0] in my_grammar.nonterminals and expr[1] in my_grammar.nonterminals)

    def test_to_cnf_to_file_written_correctly(self):
        self.test_dir = tempfile.gettempdir()
        f = open(path.join(self.test_dir, 'input.txt'), 'w')
        f.write('\n'.join(rules))
        f.close()
        to_cnf_to_file(path.join(self.test_dir, 'input.txt'), path.join(self.test_dir, 'output.txt'))
        f = open(path.join(self.test_dir, 'output.txt'))
        self.assertIsNotNone(f)
        written_rules = f.readlines()
        f.close()
        self.assertTrue(all(len(rule.split()) >= 2 for rule in written_rules))
        self.assertTrue(all(rule.split()[0][0].isupper() for rule in written_rules))

    def test_to_cnf_to_file_is_cnf(self):
        self.test_dir = tempfile.gettempdir()
        f = open(path.join(self.test_dir, 'input.txt'), 'w')
        f.write('\n'.join(rules))
        f.close()
        to_cnf_to_file(path.join(self.test_dir, 'input.txt'), path.join(self.test_dir, 'output.txt'))
        f = open(path.join(self.test_dir, 'output.txt'))
        new_rules = f.readlines()
        f.close()
        my_grammar = CFGrammar(new_rules)
        for nonterminal, expr in my_grammar.rules:
            self.assertLessEqual(len(expr), 2)
            self.assertFalse(my_grammar.start_nonterminal in expr)
            if expr == ['eps']:
                self.assertTrue(nonterminal == my_grammar.start_nonterminal)
            if len(expr) == 1:
                self.assertTrue(expr[0] in my_grammar.terminals)
            if len(expr) == 2:
                self.assertTrue(expr[0] in my_grammar.nonterminals and expr[1] in my_grammar.nonterminals)

    def test_correct_bracket_sequence_example(self):
        my_grammar = CFGrammar(cbs_rules)
        my_grammar.to_cnf()
        self.assertEqual(my_grammar.start_nonterminal, 'S')
        sorted_rules = my_grammar.rules
        sorted_rules.sort()
        self.assertEqual(sorted_rules,
                         [('A0', ['A5', 'A7']),
                          ('A0', ['A7', 'A1']),
                          ('A0', ['b']),
                          ('A1', ['A4', 'A7']),
                          ('A1', ['b']),
                          ('A3', ['a']),
                          ('A4', ['b']),
                          ('A5', ['b']),
                          ('A6', ['a']),
                          ('A7', ['A3', 'A0']),
                          ('S', ['A6', 'A0']),
                          ('S', ['eps']),
                          ])


if __name__ == '__main__':
    unittest.main()
