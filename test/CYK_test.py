import io
import unittest.mock
import tempfile
import unittest
from os import path

from src.CYK import *
from Grammars_n_graphs import deterministic_cbs_rules, ambiguous_cbs_rules, inherently_ambiguous_grammar


class TestCYK(unittest.TestCase):
    def test_cyk_on_deterministic_grammar(self):
        grammar = CFGrammar(deterministic_cbs_rules)
        self.assertTrue(cyk(grammar, '(())()'))
        self.assertTrue(cyk(grammar, ''))
        self.assertFalse(cyk(grammar, '()(('))

    def test_cyk_on_ambiguous_grammar(self):
        grammar = CFGrammar(ambiguous_cbs_rules)
        self.assertTrue(cyk(grammar, '(())()'))
        self.assertTrue(cyk(grammar, ''))
        self.assertFalse(cyk(grammar, '()(('))

    def test_cyk_on_inherently_ambiguous_grammar(self):
        grammar = CFGrammar(inherently_ambiguous_grammar)
        self.assertTrue(cyk(grammar, 'aaaabbbbc'))
        self.assertTrue(cyk(grammar, 'aaaabbbb'))
        self.assertTrue(cyk(grammar, 'abbbbcccc'))
        self.assertTrue(cyk(grammar, 'c'))
        self.assertTrue(cyk(grammar, ''))
        self.assertTrue(cyk(grammar, 'aabbccccccccc'))
        self.assertTrue(cyk(grammar, 'aaaaaaabc'))
        self.assertTrue(cyk(grammar, 'bc'))
        self.assertTrue(cyk(grammar, 'a'))
        self.assertFalse(cyk(grammar, 'abcabc'))
        self.assertFalse(cyk(grammar, 'cab'))
        self.assertFalse(cyk(grammar, 'aaabbccc'))
        self.assertFalse(cyk(grammar, 'abcd'))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_accepts_on_ambiguous_grammar_good_string(self, mock_stdout):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in ambiguous_cbs_rules:
            rf.write(rule + '\n')
        rf.close()
        good_string_file = path.join(self.test_dir, 'goodstr.txt')
        goodsf = open(good_string_file, 'w')
        goodsf.write('(())()')
        goodsf.close()

        accepts(grammar_file, good_string_file)
        self.assertEqual(mock_stdout.getvalue(), 'Accepts\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_accepts_on_ambiguous_grammar_bad_string(self, mock_stdout):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in ambiguous_cbs_rules:
            rf.write(rule + '\n')
        rf.close()

        bad_string_file = path.join(self.test_dir, 'badstr.txt')
        badsf = open(bad_string_file, 'w')
        badsf.write('()((')
        badsf.close()

        accepts(grammar_file, bad_string_file)
        self.assertEqual(mock_stdout.getvalue(), 'Does not accept\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_accepts_on_ambiguous_grammar_empty_string(self, mock_stdout):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in ambiguous_cbs_rules:
            rf.write(rule + '\n')
        rf.close()

        empty_string_file = path.join(self.test_dir, 'emptystr.txt')
        emptysf = open(empty_string_file, 'w')
        emptysf.close()

        accepts(grammar_file, empty_string_file)
        self.assertEqual(mock_stdout.getvalue(), 'Accepts\n')


if __name__ == '__main__':
    unittest.main()
