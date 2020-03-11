import unittest
import tempfile
from pprint import pprint

from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF
from os import path


class TestRDF(unittest.TestCase):

    def test_file_system(self):
        self.test_dir = tempfile.gettempdir()
        f = open(path.join(self.test_dir, 'test.txt'), 'w')
        f.write('The owls are not what they seem')
        f.close()
        f = open(path.join(self.test_dir, 'test.txt'))
        self.assertEqual(f.read(), 'The owls are not what they seem')
        f.close()

    def test_reading_nt_file(self):
        self.test_dir = tempfile.gettempdir()
        filename = path.join(self.test_dir, 'demo.nt')
        f = open(filename, 'w')
        f.write("<http://bigasterisk.com/foaf.rdf#drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                "<http://xmlns.com/foaf/0.1/Person> .\n" +
                '<http://bigasterisk.com/foaf.rdf#drewp> <http://example.com/says> "Hello world" .')
        f.close()
        g = Graph()
        g.parse(filename, format="nt")
        self.assertEqual(len(g), 2)

    def test_add(self):
        bob = BNode()
        name = Literal('Bob')

        g = Graph()

        g.add((bob, RDF.type, FOAF.Person))
        g.add((bob, FOAF.name, name))
        g.add((bob, FOAF.age, Literal(42)))

        self.assertEqual(len(g), 3)
        self.assertEqual(int(g.value(bob, FOAF.age)), 42)

    def test_set(self):
        linda = BNode()
        g = Graph()
        g.add((linda, FOAF.age, Literal(42)))
        self.assertEqual(int(g.value(linda, FOAF.age)), 42)
        g.set((linda, FOAF.age, Literal(43)))
        self.assertEqual(int(g.value(linda, FOAF.age)), 43)

    def test_remove(self):
        bob = URIRef("http://example.org/people/Bob")
        linda = BNode()
        name = Literal('Bob')

        g = Graph()

        g.add((bob, RDF.type, FOAF.Person))
        g.add((bob, FOAF.name, name))
        g.add((bob, FOAF.knows, linda))
        g.add((linda, RDF.type, FOAF.Person))
        g.add((linda, FOAF.name, Literal('Linda')))
        g.add((bob, FOAF.age, Literal(42)))

        self.assertEqual(len(g), 6)
        g.remove((bob, None, None))
        self.assertEqual(len(g), 2)


if __name__ == '__main__':
    unittest.main()
