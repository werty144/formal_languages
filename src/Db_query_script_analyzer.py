import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees
from gen.graph_query_grammarLexer import graph_query_grammarLexer
from gen.graph_query_grammarParser import graph_query_grammarParser
from gen.graph_query_grammarListener import graph_query_grammarListener


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def edge(self, source, target):
        self.edges.append((source, target))

    def to_string(self):
        return "edges: %s, functions: %s" % (str(self.edges), self.nodes)

    def to_DOT(self):
        buf = ''.join(["graph G{\n", "  ranksep=.25;\n", "  edge [arrowsize=.5]\n",
                       "  node [shape=plaintext, fontname=\"ArialNarrow\",\n",
                       "        fontsize=12, fixedsize=true, height=.30];\n"])
        for node, label in self.nodes:
            buf = ''.join([buf, "  ", f'{node} [label="{label}"]\n'])
        for src, trg in self.edges:
            buf = ''.join([buf, "  ", str(src), " -- ", str(trg), ";\n"])
        buf = buf + "}\n"
        return buf


class FunctionListener(graph_query_grammarListener):
    def __init__(self, start_type):
        self.graph = Graph()
        self.node_counter = -1
        self.stack = []
        self.start_type = start_type

    def enterEveryRule(self,  ctx: ParserRuleContext):
        rule_type = str(type(ctx)).split('.')[-1][:-9]
        self.node_counter += 1
        cur_node = self.node_counter
        self.graph.nodes.append((cur_node, rule_type))
        if rule_type != self.start_type:
            self.graph.edge(self.stack[-1], self.node_counter)
        self.stack.append(cur_node)

        for child in ctx.getChildren():
            if isinstance(child, TerminalNodeImpl):
                symb = str(child.getSymbol()).split("'")[1]
                self.node_counter += 1
                self.graph.nodes.append((self.node_counter, symb))
                self.graph.edge(cur_node, self.node_counter)

    def exitEveryRule(self, ctx):
        self.stack.pop()


def main(argv):
    if argv[1] == '--file':
        input_file = argv[2]
        input_stream = FileStream(input_file)
        out_file = argv[3]
    elif argv[1] == '--stdin':
        input_stream = StdinStream()
        out_file = argv[2]
    else:
        print('Usage: [--file <file_name> | --stdin] <output_file>')
        return

    lexer = graph_query_grammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = graph_query_grammarParser(stream)
    parser.removeErrorListeners()
    tree = parser.script()
    if parser.getNumberOfSyntaxErrors() > 0:
        print('Failed')
        return

    print('Success')
    walker = ParseTreeWalker()
    collector = FunctionListener('Script')
    walker.walk(collector, tree)
    fout = open(out_file, 'w')
    fout.write(collector.graph.to_DOT())
    fout.close()


if __name__ == '__main__':
    main(sys.argv)
