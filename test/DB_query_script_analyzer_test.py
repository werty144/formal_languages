import unittest
import tempfile
from os import path
from unittest.mock import patch
from io import StringIO

from src.Db_query_script_analyzer import *

dot_header = 'graph G{\n' \
             '  ranksep=.25;\n' \
             '  edge [arrowsize=.5]\n' \
             '  node [shape=plaintext, fontname="ArialNarrow",\n' \
             '        fontsize=12, fixedsize=true, height=.30];\n'

correct_dot_s1 = dot_header + \
                '  0 [label="label1"]\n' \
                '  1 [label="label2"]\n' \
                '  0 -- 1;\n' \
                '}\n'

correct_dot_s2 = dot_header + \
                '  0 [label="Script"]\n'\
                '  1 [label=";"]\n'\
                '  2 [label="Stmt"]\n'\
                '  3 [label="CONNECT"]\n'\
                '  4 [label="TO"]\n'\
                '  5 [label="[myfile]"]\n'\
                '  0 -- 1;\n'\
                '  0 -- 2;\n'\
                '  2 -- 3;\n'\
                '  2 -- 4;\n'\
                '  2 -- 5;\n'\
                '}\n'

empty_input_dot = dot_header +\
                '  0 [label="Script"]\n'\
                '  1 [label="<EOF>"]\n'\
                '  0 -- 1;\n'\
                '}\n'


class Buffer:
    def __init__(self, s):
        self.b = bytearray(s, 'ascii')

    def read(self):
        return self.b


class Mystdin:
    def __init__(self, s):
        self.buffer = Buffer(s)


class TestDBQueryScriptAnalyzer(unittest.TestCase):
    def test_toDot(self):
        graph = Graph()
        graph.nodes.append((0, 'label1'))
        graph.nodes.append((1, 'label2'))
        graph.edge(0, 1)
        dot_s = graph.to_DOT()
        self.assertEqual(correct_dot_s1, dot_s)

    @patch("sys.stdin", Mystdin("CONNECT TO [myfile];"))
    def test_Function_Listener(self):
        lexer = graph_query_grammarLexer(StdinStream())
        stream = CommonTokenStream(lexer)
        parser = graph_query_grammarParser(stream)
        parser.removeErrorListeners()
        tree = parser.script()
        walker = ParseTreeWalker()
        collector = FunctionListener('Script')
        walker.walk(collector, tree)

        self.assertEqual(correct_dot_s2, collector.graph.to_DOT())

    @patch("sys.stdin", Mystdin("CONNECT TO [myfile];"))
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_on_stdin(self, mock_out):
        self.test_dir = tempfile.gettempdir()
        out_file = path.join(self.test_dir, 'out.dot')
        main([None, '--stdin', out_file])
        of = open(out_file, 'r')
        dot_s = of.read()
        of.close()
        self.assertEqual(correct_dot_s2, dot_s)
        self.assertEqual('Success\n', mock_out.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_on_file(self, mock_out):
        self.test_dir = tempfile.gettempdir()
        out_file = path.join(self.test_dir, 'out.dot')
        in_file = path.join(self.test_dir, 'input')
        inf = open(in_file, 'w')
        inf.write("CONNECT TO [myfile];")
        inf.close()
        main([None, '--file', in_file, out_file])
        of = open(out_file, 'r')
        dot_s = of.read()
        of.close()
        self.assertEqual(correct_dot_s2, dot_s)
        self.assertEqual('Success\n', mock_out.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_fail(self, mock_out):
        self.test_dir = tempfile.gettempdir()
        out_file = path.join(self.test_dir, 'out.dot')
        in_file = path.join(self.test_dir, 'input')
        inf = open(in_file, 'w')
        inf.write("CONNECT TO [myfile]")
        inf.close()
        main([None, '--file', in_file, out_file])
        self.assertEqual('Failed\n', mock_out.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty(self, mock_out):
        self.test_dir = tempfile.gettempdir()
        out_file = path.join(self.test_dir, 'out.dot')
        in_file = path.join(self.test_dir, 'input')
        inf = open(in_file, 'w')
        inf.write("")
        inf.close()
        main([None, '--file', in_file, out_file])
        of = open(out_file, 'r')
        dot_s = of.read()
        of.close()
        self.assertEqual(empty_input_dot, dot_s)
        self.assertEqual('Success\n', mock_out.getvalue())


if __name__ == '__main__':
    unittest.main()
