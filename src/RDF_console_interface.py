from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF
from rdflib.util import guess_format
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, Symbol, State
from pyformlang.regular_expression import Regex
from os import path
from typing import List
from src.DFA import rdf_to_dfa, dfa_to_dot, regex_to_minimal_dfa
import re

exit_flag = False
cur_rdf_graph: Graph
cur_dfa: DeterministicFiniteAutomaton


def print_help(args):
    print("privet")


def set_exit_flag(args):
    global exit_flag
    exit_flag = True


def load_local_rdf_file(args: List[str]):
    if len(args) == 0:
        raise Exception("Not enough args")
    global cur_rdf_graph
    cur_rdf_graph = Graph().parse(args[0], format=guess_format(args[0]))
    global cur_dfa
    cur_dfa = rdf_to_dfa(cur_rdf_graph)


def show_edge_labels(args):
    for _, label, _ in cur_rdf_graph:
        print(label)


def accept_req(args: List[str]):
    print(cur_dfa.accepts(''.join(args)))


def final_state_req(args: List[str]):
    print(cur_dfa.is_final_state(State(Literal(args[0]))))


def make_good_str(s):
    s = ''.join(list(map(lambda x: '' if (x in "|+*.$") else x, list(s))))
    return s


def intersect_with_regex(args: List[str]):
    regex = ' '.join(list(args[0]))
    file_name = args[1]
    dfa = regex_to_minimal_dfa(regex).get_intersection(cur_dfa)
    dfa_to_dot(dfa, file_name)


cases = {
    "exit": set_exit_flag,
    "help": print_help,
    "-h": print_help,
    "load_local": load_local_rdf_file,
    "show_labels": show_edge_labels,
    "does_accept": accept_req,
    "is_final_state": final_state_req,
    "intersection": intersect_with_regex,
    "mgs": make_good_str
}


def main():
    while not exit_flag:
        req = input().split()
        try:
            cases[req[0]](req[1:])
        except Exception as e:
            print(e.args[0])


if __name__ == "__main__":
    main()