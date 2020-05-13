import unittest
import os
import tempfile
from unittest.mock import patch
from io import StringIO

from Grammars_n_graphs import *
import src.query_processing
from antlr4 import *

from gen.query_languages.graph_query_grammarListener import graph_query_grammarParser
from gen.query_languages.graph_query_grammarLexer import graph_query_grammarLexer


def make_graph_folder(tmpdir):
    graph_path = os.path.join(tmpdir, 'graphs')
    os.mkdir(graph_path)
    g1file_path = os.path.join(graph_path, 'g1.txt')
    g1file = open(g1file_path, 'w')
    g1file.writelines([line + '\n' for line in syllabus_graph_triples1])
    g1file.close()
    g2file_path = os.path.join(graph_path, 'g2.txt')
    g2file = open(g2file_path, 'w')
    g2file.writelines([line + '\n' for line in my_abc_graph_triples])
    g2file.close()
    open(os.path.join(graph_path, 'empty.txt'), 'a').close()
    return graph_path


def make_scrypt_file(directory, scrypt_lines):
    scrypt_file = os.path.join(directory, 'scrypt.txt')
    scrypt_f = open(scrypt_file, 'w')
    scrypt_f.writelines(scrypt_lines)
    scrypt_f.close()
    return scrypt_file


def get_visitor(scrypt_file):
    input_stream = FileStream(scrypt_file)
    lexer = graph_query_grammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = graph_query_grammarParser(stream)
    parser.removeErrorListeners()
    tree = parser.script()
    visitor = src.query_processing.queryVisitor()
    visitor.visit(tree)
    return visitor


class QueryProcessingTest(unittest.TestCase):

    def test_connect(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            visitor = get_visitor(scrypt_file)
            self.assertEqual(graph_dir, visitor.cur_graph_dir)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_in_main(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];', 'LIST ALL GRAPHS;']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            src.query_processing.main([None, '--file', scrypt_file])
        output = mock.getvalue()
        correct = 'g1.txt\nempty.txt\ng2.txt\n'
        self.assertEqual(correct, output)

    def test_named_pattern_without_regex(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = ['S = a S b S;', 'S = eps;']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            visitor = get_visitor(scrypt_file)
            correct = ['S a S b S', 'S eps']
            self.assertEqual(correct, visitor.rules)

    def test_named_pattern_with_regex(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = ['S = a S b S | eps;', 'A = a* b* ;']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            visitor = get_visitor(scrypt_file)
            correct = ['S a S b S | eps', 'A (a)* (b)*']
            self.assertEqual(correct, visitor.rules)

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_pair_true(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | eps;\n',
                            'SELECT EXISTS((u, v)) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'True\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_pair_false(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = c | d;\n',
                            'SELECT EXISTS((u, v)) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'False\n'
            self.assertTrue(correct, mock.getvalue())

    def test_select_exists_pair_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | eps;\n',
                            'SELECT EXISTS((u, v)) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u.ID = 1) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            with self.assertRaises(src.query_processing.BadScriptException) as bs:
                get_visitor(scrypt_file)
            self.assertEqual('Condition on fix variable', bs.exception.message)

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_from_id_true(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u.ID = 1) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'True\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_from_id_false(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u.ID = 2) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'False\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_from_underscore_true(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (_) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'True\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_from_underscore_false(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | c;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (_) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'False\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_from_random(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b | a b;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (RANDOM) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            true_cnt = 0
            false_cnt = 0
            for _ in range(100):
                get_visitor(scrypt_file)
                last_mock = list(filter(lambda s: s != '', mock.getvalue().split('\n')))[-1]
                if last_mock == 'True':
                    true_cnt += 1
                else:
                    false_cnt += 1
            self.assertGreater(true_cnt, 50)
            self.assertGreater(false_cnt, 10)

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_to_id_true(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (v.ID = 3);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'True\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_to_id_false(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (v.ID = 1);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'False\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_to_underscore_true(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | a b;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (_);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'True\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_to_underscore_false(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | c;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (_);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            get_visitor(scrypt_file)
            correct = 'False\n'
            self.assertEqual(correct, mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_select_exists_unit_to_random(self, mock):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b | a b;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u) - S -> (RANDOM);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            true_cnt = 0
            false_cnt = 0
            for _ in range(100):
                get_visitor(scrypt_file)
                last_mock = list(filter(lambda s: s != '', mock.getvalue().split('\n')))[-1]
                if last_mock == 'True':
                    true_cnt += 1
                else:
                    false_cnt += 1
            self.assertGreater(true_cnt, 30)
            self.assertGreater(false_cnt, 30)

    def test_select_exists_unit_to_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | eps;\n',
                            'SELECT EXISTS(u) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (z) - S -> (v);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            with self.assertRaises(src.query_processing.BadScriptException) as bs:
                get_visitor(scrypt_file)
            self.assertEqual('Unknown variable', bs.exception.message)

    def test_select_exists_unit_from_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_dir = make_graph_folder(tmpdir)
            scrypt_dir = tmpdir
            scrypt_lines = [f'CONNECT TO [{graph_dir}];\n', 'S = a S b S | eps;\n',
                            'SELECT EXISTS(v) FROM' + ' [' + os.path.join(graph_dir, 'g1.txt]') + ' ' +
                            'WHERE (u.ID = 1) - S -> (z);']
            scrypt_file = make_scrypt_file(scrypt_dir, scrypt_lines)
            with self.assertRaises(src.query_processing.BadScriptException) as bs:
                get_visitor(scrypt_file)
            self.assertEqual('Unknown variable', bs.exception.message)


if __name__ == '__main__':
    unittest.main()
