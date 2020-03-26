class CFGrammar:
    def __init__(self, rules):
        self.rules = []
        self.nonterminals = []
        self.terminals = ['eps']
        self.start_nonterminal = 'S'
        for rule in rules:
            nonterminal = rule.split()[0]
            expr = rule.split()[1:]
            self.add_rule(nonterminal, expr)

    def print_rules(self):
        for nonterminal, expr in self.rules:
            print(nonterminal, "->", ' '.join(expr))

    def print_terminals(self):
        print("Terminals:", end=' ')
        for terminal in self.terminals:
            print(terminal, end=' ')
        print()

    def print_nonterminals(self):
        print("Nonterminals:", end=' ')
        for nonterminal in self.nonterminals:
            print(nonterminal, end=' ')
        print()

    def add_rule(self, nonterminal, expr):
        if (nonterminal, expr) in self.rules:
            return
        self.rules.append((nonterminal, expr))
        if nonterminal not in self.nonterminals:
            self.nonterminals.append(nonterminal)
        for symbol in expr:
            if symbol[0].isupper():
                if symbol not in self.nonterminals:
                    self.nonterminals.append(symbol)
            else:
                if symbol not in self.terminals:
                    self.terminals.append(symbol)

    def get_fresh_nonterminal(self):
        i = 0
        while 'A' + str(i) in self.nonterminals:
            i += 1
        return 'A' + str(i)

    def get_rid_of_long_rules(self):
        for nonterminal, expr in self.rules:
            if len(expr) <= 2:
                continue
            last = nonterminal
            for symbol in expr[:len(expr) - 2]:
                fresh_nonterminal = self.get_fresh_nonterminal()
                self.add_rule(last, [symbol, fresh_nonterminal])
                last = fresh_nonterminal
            self.add_rule(last, expr[len(expr) - 2:])
            self.rules.remove((nonterminal, expr))

    def get_eps_producing_nonterminals(self):
        eps_producing_nonterminals = []
        for nonterminal, expr in self.rules:
            if expr == ['eps']:
                eps_producing_nonterminals.append(nonterminal)
        some_left = True
        while some_left:
            some_left = False
            for nonterminal, expr in self.rules:
                if nonterminal in eps_producing_nonterminals:
                    continue
                if all(symbol in eps_producing_nonterminals for symbol in expr):
                    eps_producing_nonterminals.append(nonterminal)
                    some_left = True
        return eps_producing_nonterminals

    def get_rid_of_eps_rules(self):
        eps_producing_nonterminals = self.get_eps_producing_nonterminals()
        for nonterminal, expr in self.rules:
            if len(expr) == 1:
                if expr[0] in eps_producing_nonterminals:
                    self.add_rule(nonterminal, ['eps'])
                continue
            if expr[0] in eps_producing_nonterminals:
                if expr[1] in eps_producing_nonterminals:
                    self.add_rule(nonterminal, [expr[1]])
                    self.add_rule(nonterminal, [expr[0]])
                    self.add_rule(nonterminal, ['eps'])
                else:
                    self.add_rule(nonterminal, [expr[1]])
            elif expr[1] in eps_producing_nonterminals:
                self.add_rule(nonterminal, [expr[0]])

        was_eps_rules = False
        for nonterminal, expr in self.rules.copy():
            if expr == ['eps']:
                was_eps_rules = True
                self.rules.remove((nonterminal, expr))
        if was_eps_rules:
            new_s = self.get_fresh_nonterminal()
            self.add_rule(new_s, ['eps'])
            self.add_rule(new_s, [self.start_nonterminal])
            self.start_nonterminal = new_s

    def dfs(self, u, used, edges):
        used.append(u)
        for v in edges[u]:
            if v not in used:
                used = self.dfs(v, used, edges)
        return used

    def get_rid_of_chain_rules(self):
        edges = {}
        for nonterminal in self.nonterminals:
            edges[nonterminal] = []
        for nonterminal, expr in self.rules:
            if len(expr) == 1 and expr[0] in self.nonterminals:
                edges[nonterminal].append(expr[0])
        reachable = {}
        for nonterminal in self.nonterminals:
            reachable[nonterminal] = self.dfs(nonterminal, [], edges)
        for nonterminal in self.nonterminals:
            for chain_nonterm in reachable[nonterminal]:
                for nonterm, expr in self.rules:
                    if nonterm == chain_nonterm:
                        if len(expr) > 1 or expr[0] in self.terminals:
                            self.add_rule(nonterminal, expr)
        for nonterminal, expr in self.rules.copy():
            if len(expr) == 1 and expr[0] in self.nonterminals:
                self.rules.remove((nonterminal, expr))

    def get_rid_of_useless_symbols(self):
        producing_nonterminals = []
        for nonterminal, expr in self.rules:
            if len(expr) == 1:
                if expr[0] in self.terminals:
                    producing_nonterminals.append(nonterminal)
            if len(expr) == 2:
                if expr[0] in self.terminals and expr[1] in self.terminals:
                    producing_nonterminals.append(nonterminal)
        some_left = True
        while some_left:
            some_left = False
            for nonterminal, expr in self.rules:
                if nonterminal in producing_nonterminals:
                    continue
                if all(symbol in producing_nonterminals or symbol in self.terminals for symbol in expr):
                    producing_nonterminals.append(nonterminal)
                    some_left = True
        notproducing_nonterminals = []
        for nonterminal in self.nonterminals:
            if nonterminal not in producing_nonterminals:
                notproducing_nonterminals.append(nonterminal)
        for nonterminal, expr in self.rules.copy():
            if nonterminal in notproducing_nonterminals or any(symbol in notproducing_nonterminals for symbol in expr):
                self.rules.remove((nonterminal, expr))
        for nonterminal in notproducing_nonterminals:
            self.nonterminals.remove(nonterminal)

    def make_lonely_terminals(self):
        for nonterminal, expr in self.rules.copy():
            if len(expr) == 1:
                continue
            if expr[0] in self.terminals:
                new_nonterminal1 = self.get_fresh_nonterminal()
                self.add_rule(new_nonterminal1, expr[0])
            else:
                new_nonterminal1 = expr[0]
            if expr[1] in self.terminals:
                new_nonterminal2 = self.get_fresh_nonterminal()
                self.add_rule(new_nonterminal2, expr[1])
            else:
                new_nonterminal2 = expr[1]
            self.rules.remove((nonterminal, expr))
            self.add_rule(nonterminal, [new_nonterminal1, new_nonterminal2])

    def to_cnf(self):
        self.get_rid_of_long_rules()
        self.get_rid_of_eps_rules()
        self.get_rid_of_chain_rules()
        self.get_rid_of_useless_symbols()
        self.make_lonely_terminals()


def to_cnf_to_file(infile, outfile):
    inf = open(infile, "r")
    rules = inf.readlines()
    inf.close()
    my_grammar = CFGrammar(rules)
    my_grammar.to_cnf()
    ouf = open(outfile, "w")
    for nonterminal, expr in my_grammar.rules:
        ouf.write(nonterminal + " " + ' '.join(expr) + '\n')
    ouf.close()

