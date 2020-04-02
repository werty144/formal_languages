from src.CNF import CFGrammar


def cyk(grammar: CFGrammar, s: str):
    if len(s) == 0:
        return grammar.produces_eps()
    grammar.to_cnf()
    n = len(s)
    d = []
    for i in range(n):
        d.append([])
        for j in range(n):
            d[i].append([])

    for i in range(n):
        for nonterminal, expr in grammar.rules:
            if expr[0] == s[i]:
                d[i][i].append(nonterminal)

    for l in range(2, n + 1):
        for i in range(n):
            j = min(i + l - 1, n - 1)
            for k in range(i, j):
                left = d[i][k]
                right = d[k + 1][j]
                for nonterminal, expr in grammar.rules:
                    if len(expr) == 1:
                        continue
                    if expr[0] in left and expr[1] in right:
                        d[i][j].append(nonterminal)

    return grammar.start_nonterminal in d[0][n - 1]


def accepts(grammar_file, sring_file):
    gf = open(grammar_file, 'r')
    sf = open(sring_file, 'r')
    rules = gf.readlines()
    gf.close()
    s = sf.readline()
    sf.close()
    grammar = CFGrammar(rules)
    print(cyk(grammar, s))
