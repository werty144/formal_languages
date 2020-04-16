from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import EpsilonNFA
import networkx as nx
import numpy as np
from src.CFG import CFGrammar


def regex_to_pda_graph(regex, first_node_number):
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
    i = first_node_number
    for node in sorted(graph.nodes):
        my_map[node] = i
        i += 1
    graph: nx.Graph = nx.relabel_nodes(graph, my_map)
    for edge in graph.edges:
        graph.edges[edge]['label'] = [graph.edges[edge]['label']]
    return nx.DiGraph(graph)


def make_matrix_from_graph(graph: nx.Graph):
    n = len(graph.nodes)
    arr = []
    for i in range(n):
        arr.append([])
        for j in range(n):
            arr[i].append([])
            if (i, j) in graph.edges:
                try:
                    arr[i][j].append(graph.edges[(i, j, 0)]['label'])
                except KeyError:
                    pass

    return np.array(arr)


def my_tensor_prod(g1, g2):
    res = nx.tensor_product(g1, g2)
    killing_list = []
    for edge in res.edges:
        arr1, arr2 = res.edges[edge]['label']
        if not intersection(arr1, arr2):
            killing_list.append(edge)
        else:
            res.edges[edge]['label'] = intersection(arr1, arr2)
    for edge in killing_list:
        res.remove_edge(edge[0], edge[1])
    return nx.DiGraph(res)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def reachability_using_kron(pda_graph: nx.Graph, graph: nx.Graph, get_nonterminals, grammar: CFGrammar):
    if grammar.produces_eps():
        for i in range(len(graph.nodes)):
            graph.add_edge(i, i, label=grammar.get_eps_producing_nonterminals())
    changes = True
    while changes:
        changes = False
        m3 = my_tensor_prod(pda_graph, graph)
        m3_closure = nx.transitive_closure(m3)
        for edge in m3_closure.edges(data='label'):
            s = edge[0][0]
            f = edge[1][0]
            if pda_graph.nodes[s]['is_start'] and pda_graph.nodes[f]['is_final']:
                x, y = edge[0][1], edge[1][1]
                if y not in graph[x].keys():
                    graph.add_edge(x, y, label=[get_nonterminals[s]])
                    changes = True
                elif get_nonterminals[s] not in graph[x][y]['label']:
                    changes = True
                    graph[x][y]['label'].append(get_nonterminals[s])
    return graph


def use_reachability_using_kron(grammar_file, graph_file, res_file):
    grm_file = open(grammar_file, 'r')
    grammar = CFGrammar([])
    grammar.read_hard_from_file(grammar_file)
    regexs = grm_file.read().splitlines()
    grm_file.close()
    pda_graph = nx.DiGraph()
    get_nonterminals = {}
    for regex in regexs:
        new_component = regex_to_pda_graph(regex[1:], len(pda_graph.nodes))
        pda_graph = nx.union(pda_graph, new_component)
        for node in new_component.nodes:
            get_nonterminals[node] = regex[0]

    grpf = open(graph_file, 'r')
    graph = nx.DiGraph()
    for (u, l, v) in [triple.split() for triple in grpf.read().splitlines()]:
        graph.add_edge(int(u), int(v), label=[l])
    grpf.close()
    res_graph = reachability_using_kron(pda_graph, graph, get_nonterminals, grammar)

    rf = open(res_file, 'w')
    n = len(pda_graph.nodes)
    for i in range(n):
        for j in range(n):
            if j in pda_graph[i].keys():
                rf.write(str(pda_graph[i][j]['label']))
            else:
                rf.write('.')
        rf.write('\n')
    rf.write('\n')
    for edge in res_graph.edges(data='label'):
        if 'S' in edge[2]:
            rf.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
    rf.close()
