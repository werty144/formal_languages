from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import *
from rdflib import Graph, URIRef
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot


def regex_to_minimal_dfa(regex_str):
    regex = Regex(regex_str)
    return regex.to_epsilon_nfa().minimize()


def rdf_to_dfa(graph: Graph):
    predfa = EpsilonNFA()
    start_state = State("start_state")
    predfa.add_start_state(start_state)
    state_cnt = 0
    for frm, label, to in graph:
        frm = str(frm)
        label = str(label)
        to = str(to)
        predfa.add_transition(start_state, Epsilon(), State(frm))
        predfa.add_transition(start_state, Epsilon(), State(to))
        predfa.add_final_state(State(frm))
        predfa.add_final_state(State(to))

        predfa.add_transition(State(frm), Epsilon(), State(state_cnt))
        for c in label:
            predfa.add_transition(State(state_cnt), Symbol(c), State(state_cnt + 1))
            state_cnt += 1
        predfa.add_transition(State(state_cnt), Epsilon(), State(to))

    return predfa.to_deterministic()


def dfa_to_dot(dfa: DeterministicFiniteAutomaton, filename: str):
    g = nx.DiGraph()
    for frm, edges in dfa.to_dict().items():
        for edge, to in edges.items():
            g.add_edge(str(frm), str(to), label=str(edge))
    print(f"Nodes: {len(g.nodes)}, Edges: {len(g.edges)}")
    write_dot(g, filename)
