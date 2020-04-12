from src.CFG import CFGrammar
from Graph_utils import Graph


def hellings(grammar: CFGrammar, graph: Graph):
    grammar.to_weak_cnf()
    res = []
    m = []
    for nonterminal, expr in grammar.rules:
        if not expr == ['eps']:
            continue
        for v in graph.vertices:
            res.append((nonterminal, v, v))
            m.append((nonterminal, v, v))

    for u, c, v in graph.edges:
        for nonterminal, expr in grammar.rules:
            if expr[0] == c:
                res.append((nonterminal, u, v))
                m.append((nonterminal, u, v))

    while m:
        ni, v, u = m.pop(0)
        for nj, w, pv in res:
            if pv != v:
                continue
            for nk, expr in grammar.rules:
                if len(expr) == 1:
                    continue
                if expr[0] != nj or expr[1] != ni:
                    continue
                if (nk, w, u) in res:
                    continue
                m.append((nk, w, u))
                res.append((nk, w, u))

        for nj, pu, w in res:
            if pu != u:
                continue
            for nk, expr in grammar.rules:
                if len(expr) == 1:
                    continue
                if expr[0] != ni or expr[1] != nj:
                    continue
                if (nk, v, w) in res:
                    continue
                m.append((nk, v, w))
                res.append((nk, v, w))
    return res


def use_hellings(grammar_file, graph_file, result_file):
    grmf = open(grammar_file, 'r')
    grpf = open(graph_file, 'r')
    resf = open(result_file, 'w')
    triples = grpf.readlines()
    grpf.close()
    graph = Graph(triples)
    rules = grmf.readlines()
    grmf.close()
    grammar = CFGrammar(rules)
    res = hellings(grammar, graph)
    for nonterminal, expr in grammar.rules:
        resf.write(nonterminal + ' ' + ' '.join(expr) + '\n')
    resf.write('\n')
    for nonterminal, u, v in res:
        if nonterminal == 'S':
            resf.write(str(u) + ' ' + str(v) + '\n')
    resf.close()
