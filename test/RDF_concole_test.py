import tempfile
import unittest
import sys
from io import StringIO
import src.RDF_console_interface as rdfci
from os import path


class TestRDFConsole(unittest.TestCase):

    def test_load_local_rdf_file(self):
        self.test_dir = tempfile.gettempdir()
        filename = path.join(self.test_dir, 'demo.nt')
        f = open(filename, 'w')
        f.write("<http://bigasterisk.com/foaf.rdf#drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                "<http://xmlns.com/foaf/0.1/Person> .\n" +
                '<http://bigasterisk.com/foaf.rdf#drewp> <http://example.com/says> "Hello" .')
        f.close()

        rdfci.load_local_rdf_file([filename])
        self.assertEqual(len(rdfci.cur_rdf_graph), 2)
        self.assertTrue(rdfci.cur_dfa.accepts("http://example.com/says"))

    def test_show_edge_labels(self):
        self.test_dir = tempfile.gettempdir()
        filename = path.join(self.test_dir, 'demo.nt')
        f = open(filename, 'w')
        f.write("<http://bigasterisk.com/foaf.rdf#drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                "<http://xmlns.com/foaf/0.1/Person> .\n" +
                '<http://bigasterisk.com/foaf.rdf#drewp> <http://example.com/says> "Hello" .')
        f.close()

        captured_output = StringIO()  # Create StringIO object
        sys.stdout = captured_output
        rdfci.load_local_rdf_file([filename])
        rdfci.show_edge_labels([])
        self.assertTrue(captured_output.getvalue() ==
                        "http://example.com/says\n" +
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type\n" or
                        captured_output.getvalue() ==
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type\n" +
                        "http://example.com/says\n"
                        )

        captured_output = StringIO()
        sys.stdout = captured_output

    def test_intersect_regex(self):
        self.test_dir = tempfile.gettempdir()
        in_file_name = path.join(self.test_dir, 'demo.nt')
        out_file_name = path.join(self.test_dir, 'out.dot')
        f = open(in_file_name, 'w')
        f.write("<http://bigasterisk.com/foaf.rdf#drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                "<http://xmlns.com/foaf/0.1/Person> .\n" +
                '<http://bigasterisk.com/foaf.rdf#drewp> <http://example.com/says> "Hello" .')
        f.close()

        captured_output = StringIO()
        sys.stdout = captured_output
        rdfci.load_local_rdf_file([in_file_name])

        of = open(out_file_name, 'w')
        rdfci.intersect_with_regex(["http://www.w3.org/1999/02/22-rdf-syntax-ns#type", out_file_name])
        cap = captured_output.getvalue().split()
        self.assertEqual(len(cap), 4)
        self.assertTrue(int(cap[1][0:len(cap[1]) - 1]) > 0)
        of.close()
        of = open(out_file_name, 'r')
        self.assertTrue(len(of.readlines()) > 2)
        of.close()

        captured_output = StringIO()
        sys.stdout = captured_output

        of = open(out_file_name, 'w')
        rdfci.intersect_with_regex(["http://example.com/says", out_file_name])
        cap = captured_output.getvalue().split()
        self.assertEqual(len(cap), 4)
        self.assertTrue(int(cap[1][0:len(cap[1]) - 1]) > 0)
        of.close()
        of = open(out_file_name, 'r')
        self.assertTrue(len(of.readlines()) > 2)
        of.close()

        captured_output = StringIO()
        sys.stdout = captured_output

        of = open(out_file_name, 'w')
        rdfci.intersect_with_regex(["abcaba", out_file_name])
        cap = captured_output.getvalue().split()
        self.assertEqual(len(cap), 4)
        self.assertEqual(int(cap[1][0:len(cap[1]) - 1]), 0)
        of.close()
        of = open(out_file_name, 'r')
        self.assertEqual(len(of.readlines()), 2)
        of.close()

        captured_output = StringIO()
        sys.stdout = captured_output


if __name__ == '__main__':
    unittest.main()
