from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import EpsilonNFA
import networkx as nx
import numpy as np
from src.CFG import CFGrammar
from src.CF_reachability import Nonterminal_set


def regex_to_pda_graph(regex):
    regex = Regex(regex)
    nfa: EpsilonNFA = regex.to_epsilon_nfa().minimize()
    graph: nx.MultiDiGraph = nfa.to_networkx()
    killing_list = []
    for node in graph.nodes:
        if not graph.nodes[node]['label']:
            killing_list.append(node)
    for node in killing_list:
        graph.remove_node(node)
    my_map = {}
    i = 0
    for node in sorted(graph.nodes):
        my_map[node] = i
        i += 1
    graph: nx.Graph = nx.relabel_nodes(graph, my_map)
    return graph


def make_matrix_from_graph(graph: nx.Graph, grammar: CFGrammar):
    n = len(graph.nodes)
    arr = []
    for i in range(n):
        arr.append([])
        for j in range(n):
            arr[i].append(Nonterminal_set(grammar.rules))
            if (i, j) in graph.edges:
                try:
                    arr[i][j].add_nonterminal(graph.edges[(i, j, 0)]['label'])
                except KeyError:
                    pass

    matrix = np.array(arr)
    print(matrix)


g = regex_to_pda_graph('(a b) | (a S b)')
print(g.nodes(data='is_start'))
print(g.nodes(data='is_final'))
print(g.edges(data=True))

grammar = CFGrammar([])
grammar.read_hard_from_file('input')

make_matrix_from_graph(g, grammar)

#
# a1 = np.array([[1, 0], [0, 1]])
# a2 = np.array([[1, 2], [3, 4]])
# print(np.kron(a1, a2))
