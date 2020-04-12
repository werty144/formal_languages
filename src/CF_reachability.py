from src.CFG import CFGrammar
import numpy as np
from Grammars_n_graphs import *
from src.Graph_utils import Graph


class Nonterminal_set:
    def __init__(self, rules, nonterminals=None):
        if nonterminals is None:
            nonterminals = []
        self.rules = rules
        self.nonterminals = nonterminals

    def __add__(self, other):
        return Nonterminal_set(rules=self.rules, nonterminals=list(set(self.nonterminals) | set(other.nonterminals)))

    def __mul__(self, other):
        ans = Nonterminal_set(rules=self.rules)
        for nonterminal, expr in self.rules:
            if len(expr) == 1:
                continue
            if expr[0][0].islower() or expr[1][0].islower():
                continue
            if expr[0] in self.nonterminals and expr[1] in other.nonterminals:
                ans.add_nonterminal(nonterminal)
        return ans

    def __str__(self):
        return str(self.nonterminals)

    def __repr__(self):
        return str(self.nonterminals)

    def __eq__(self, other):
        return sorted(self.nonterminals) == sorted(other.nonterminals)

    def add_nonterminal(self, nonterminal):
        if nonterminal not in self.nonterminals:
            self.nonterminals.append(nonterminal)


def reachability_using_matrix(grammar: CFGrammar, graph: Graph):
    grammar.to_weak_cnf()
    n = graph.vertices_amount()
    a = []
    for _ in range(n):
        a.append([])
        for _ in range(n):
            a[-1].append(Nonterminal_set(grammar.rules))
    t = np.array(a, dtype=Nonterminal_set)
    if grammar.produces_eps():
        for i in range(n):
            t[i, i].add_nonterminal('S')
    for i, x, j in graph.edges:
        for nonterminal, expr in grammar.rules:
            if len(expr) == 1 and expr[0] == x:
                t[i, j].add_nonterminal(nonterminal)
    changes = True
    while changes:
        changes = False
        old_t = t.copy()
        t = t + np.dot(t, t)
        if not np.array_equal(t, old_t):
            changes = True
    return [[s.nonterminals for s in row] for row in t.tolist()]


def use_reachability_using_matrix(grammar_file, graph_file, result_file):
    grmf = open(grammar_file, 'r')
    grpf = open(graph_file, 'r')
    resf = open(result_file, 'w')
    triples = grpf.readlines()
    grpf.close()
    graph = Graph(triples)
    rules = grmf.readlines()
    grmf.close()
    grammar = CFGrammar(rules)
    res = reachability_using_matrix(grammar, graph)
    for nonterminal, expr in grammar.rules:
        resf.write(nonterminal + ' ' + ' '.join(expr) + '\n')
    resf.write('\n')
    n = graph.vertices_amount()
    for i in range(n):
        for j in range(n):
            if 'S' in res[i][j]:
                resf.write(str(i) + ' ' + str(j) + '\n')
    resf.close()


def main():
    graph = Graph(my_bracket_graph_triples)
    grammar = CFGrammar(deterministic_cbs_rules)
    for huy in reachability_using_matrix(grammar, graph):
        print(huy)


if __name__ == '__main__':
    main()
