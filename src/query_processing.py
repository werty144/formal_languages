import sys
import os

from gen.query_languages.graph_query_grammarListener import graph_query_grammarListener, graph_query_grammarParser
from gen.query_languages.graph_query_grammarLexer import graph_query_grammarLexer
from antlr4 import *


class queryProcessor(graph_query_grammarListener):
    def __init__(self, start_type):
        self.start_type = start_type
        self.cur_graph_dir = ''
        self.patterns = {}

    def enterStmt(self, ctx: graph_query_grammarParser.StmtContext):
        if ctx.Kw_connect() is not None:
            self.process_connect(ctx)
        if ctx.Kw_list() is not None:
            self.process_list()
        if ctx.named_pattern() is not None:
            self.process_named_pattern(ctx)

    def process_connect(self, ctx: graph_query_grammarParser.StmtContext):
        self.cur_graph_dir = str(ctx.String())[1:-1]

    def process_list(self):
        for _, _, file_list in os.walk(self.cur_graph_dir):
            for name in file_list:
                print(name)

    def process_named_pattern(self, ctx: graph_query_grammarParser.StmtContext):
        named_pattern_ctx: graph_query_grammarParser.Named_patternContext = ctx.named_pattern()
        nt_name = named_pattern_ctx.Nt_name().getText()
        pattern_ctx: graph_query_grammarParser.PatternContext = named_pattern_ctx.pattern()
        pattern = self.enterPattern(pattern_ctx)
        self.patterns[nt_name] = pattern

    def enterPattern(self, ctx: graph_query_grammarParser.PatternContext):
        if ctx.Mid() is not None:
            return self.enterAlt_elem(ctx.alt_elem()) + ' | ' + self.enterPattern(ctx.pattern())
        else:
            return self.enterAlt_elem(ctx.alt_elem())

    def enterAlt_elem(self, ctx: graph_query_grammarParser.Alt_elemContext):
        if ctx.Lbr() is not None:
            return ctx.Lbr().getText() + ctx.Rbr().getText()
        else:
            return self.enterSeq(ctx.seq())

    def enterSeq(self, ctx: graph_query_grammarParser.SeqContext):
        if ctx.seq() is not None:
            return self.enterSeq_elem(ctx.seq_elem()) + ' ' + self.enterSeq(ctx.seq())
        else:
            return self.enterSeq_elem(ctx.seq_elem())

    def enterSeq_elem(self, ctx: graph_query_grammarParser.Seq_elemContext):
        if ctx.Op_star() is not None:
            return '(' + self.enterPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_star().getText()
        if ctx.Op_q() is not None:
            return '(' + self.enterPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_q().getText()
        if ctx.Op_plus() is not None:
            return '(' + self.enterPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_plus().getText()
        return self.enterPrim_pattern(ctx.prim_pattern())

    def enterPrim_pattern(self, ctx: graph_query_grammarParser.Prim_patternContext):
        if ctx.pattern() is not None:
            return ctx.Lbr().getText() + self.enterPattern(ctx.pattern()) + ctx.Rbr().getText()
        if ctx.Ident() is not None:
            return ctx.Ident().getText()
        return ctx.Nt_name().getText()


def main(argv):
    if argv[1] == '--file':
        input_file = argv[2]
        input_stream = FileStream(input_file)
    elif argv[1] == '--stdin':
        input_stream = StdinStream()
    else:
        print('Usage: [--file <file_name> | --stdin]')
        return

    lexer = graph_query_grammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = graph_query_grammarParser(stream)
    parser.removeErrorListeners()
    tree = parser.script()
    if parser.getNumberOfSyntaxErrors() > 0:
        print('Incorrect scrypt')
        return

    walker = ParseTreeWalker()
    collector = queryProcessor('Script')
    walker.walk(collector, tree)


if __name__ == '__main__':
    main(sys.argv)
