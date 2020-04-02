import io
import unittest.mock
import tempfile
import unittest
from distutils.util import strtobool
from os import path

from src.CYK import *

cbs_rules = ['S A S2',
             'S eps',
             'S1 A S2',
             'S2 b',
             'S2 B S1',
             'S2 S S3',
             'S3 b',
             'S3 B S1',
             'A a',
             'B b']


class TestCYK(unittest.TestCase):
    def test_cyk(self):
        grammar = CFGrammar(cbs_rules)
        self.assertTrue(cyk(grammar, 'aabbab'))
        self.assertFalse(cyk(grammar, 'abaa'))
        self.assertTrue(cyk(grammar, ''))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_accepts(self, mock_stdout):
        self.test_dir = tempfile.gettempdir()
        grammar_file = path.join(self.test_dir, 'rules.txt')
        rf = open(grammar_file, 'w')
        for rule in cbs_rules:
            rf.write(rule + '\n')
        rf.close()
        good_string_file = path.join(self.test_dir, 'goodstr.txt')
        goodsf = open(good_string_file, 'w')
        goodsf.write('aabbab')
        goodsf.close()
        bad_string_file = path.join(self.test_dir, 'badstr.txt')
        badsf = open(bad_string_file, 'w')
        badsf.write('abaa')
        badsf.close()
        empty_string_file = path.join(self.test_dir, 'emptystr.txt')
        emptysf = open(empty_string_file, 'w')
        emptysf.close()

        accepts(grammar_file, good_string_file)
        self.assertTrue(mock_stdout.getvalue())

        accepts(grammar_file, bad_string_file)
        self.assertFalse(strtobool(mock_stdout.getvalue().split('\n')[1]))

        accepts(grammar_file, empty_string_file)
        self.assertTrue(strtobool(mock_stdout.getvalue().split('\n')[2]))


if __name__ == '__main__':
    unittest.main()
