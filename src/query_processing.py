import sys
import os
import random
from antlr4 import *

from gen.query_languages.graph_query_grammarListener import graph_query_grammarParser
from gen.query_languages.graph_query_grammarLexer import graph_query_grammarLexer
from gen.query_languages.graph_query_grammarVisitor import graph_query_grammarVisitor
from src.CFG import CFGrammar
from src.Hellings import hellings
from src.Graph_utils import Graph


class BadScriptException(Exception):
    def __init__(self, message):
        self.message = message


def is_ident(v_expr):
    if v_expr.Ident() is None:
        return False
    if v_expr.Kw_id() is not None:
        return False
    return True


class queryVisitor(graph_query_grammarVisitor):
    def __init__(self):
        self.cur_graph_dir = ''
        self.rules = []

    def visitStmt(self, ctx: graph_query_grammarParser.StmtContext):
        if ctx.Kw_connect() is not None:
            self.process_connect(ctx)
        if ctx.Kw_list() is not None:
            self.process_list()
        if ctx.named_pattern() is not None:
            self.visitNamed_pattern(ctx.named_pattern())
        if ctx.select_stmt() is not None and ctx.Kw_write() is None:
            print(self.visitSelect_stmt(ctx.select_stmt()))

    def process_connect(self, ctx: graph_query_grammarParser.StmtContext):
        self.cur_graph_dir = ctx.String().getText()[1:-1]

    def process_list(self):
        for _, _, file_list in os.walk(self.cur_graph_dir):
            for name in file_list:
                print(name)

    def visitNamed_pattern(self, ctx: graph_query_grammarParser.Named_patternContext):
        nt_name = ctx.Nt_name().getText()
        pattern_ctx: graph_query_grammarParser.PatternContext = ctx.pattern()
        pattern = self.visitPattern(pattern_ctx)
        self.rules.append(nt_name + ' ' + pattern)

    def visitPattern(self, ctx: graph_query_grammarParser.PatternContext):
        if ctx.Mid() is not None:
            return self.visitAlt_elem(ctx.alt_elem()) + ' | ' + self.visitPattern(ctx.pattern())
        else:
            return self.visitAlt_elem(ctx.alt_elem())

    def visitAlt_elem(self, ctx: graph_query_grammarParser.Alt_elemContext):
        if ctx.Lbr() is not None:
            return ctx.Lbr().getText() + ctx.Rbr().getText()
        else:
            return self.visitSeq(ctx.seq())

    def visitSeq(self, ctx: graph_query_grammarParser.SeqContext):
        if ctx.seq() is not None:
            return self.visitSeq_elem(ctx.seq_elem()) + ' ' + self.visitSeq(ctx.seq())
        else:
            return self.visitSeq_elem(ctx.seq_elem())

    def visitSeq_elem(self, ctx: graph_query_grammarParser.Seq_elemContext):
        if ctx.Op_star() is not None:
            return '(' + self.visitPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_star().getText()
        if ctx.Op_q() is not None:
            return '(' + self.visitPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_q().getText()
        if ctx.Op_plus() is not None:
            return '(' + self.visitPrim_pattern(ctx.prim_pattern()) + ')' + ctx.Op_plus().getText()
        return self.visitPrim_pattern(ctx.prim_pattern())

    def visitPrim_pattern(self, ctx: graph_query_grammarParser.Prim_patternContext):
        if ctx.pattern() is not None:
            return ctx.Lbr().getText() + self.visitPattern(ctx.pattern()) + ctx.Rbr().getText()
        if ctx.Ident() is not None:
            return ctx.Ident().getText()
        return ctx.Nt_name().getText()

    def visitSelect_stmt(self, ctx: graph_query_grammarParser.Select_stmtContext):
        s_acceptable, graph_vertices_amount = self.get_s_acceptable(ctx)
        vs_info = ctx.obj_expr().vs_info()[0].Ident()
        from_expr = ctx.where_expr().v_expr()[0]
        to_expr = ctx.where_expr().v_expr()[1]
        try:
            if ctx.obj_expr().Kw_exists() is not None:
                return self.process_exists(vs_info, from_expr, to_expr, s_acceptable, graph_vertices_amount)
        except BadScriptException as e:
            raise e

    def get_s_acceptable(self, ctx: graph_query_grammarParser.Select_stmtContext):
        graph_file = ctx.String().getText()[1:-1]
        gf = open(graph_file, 'r')
        graph_triples = gf.readlines()
        gf.close()
        graph = Graph(graph_triples)
        pattern = self.visitPattern(ctx.where_expr().pattern())
        grammar = CFGrammar([])
        grammar.add_hard_rule(f'S {pattern}')
        for rule in self.rules:
            grammar.add_hard_rule(rule)
        s_acceptable = list(filter(lambda x: x is not None,
                                   [(triple[1], triple[2]) if triple[0] == 'S' else None
                                    for triple in hellings(grammar, graph)
                                    ]
                                   ))
        return s_acceptable, len(graph.vertices)

    @staticmethod
    def process_exists(vs_info, from_expr, to_expr, s_acceptable, graph_vertices_amount):
        if len(vs_info) == 2:
            if not (is_ident(from_expr) and is_ident(to_expr)):
                raise BadScriptException('Condition on fix variable')
            return len(s_acceptable) > 0
        # if one variable
        v_name = vs_info[0].getText()
        if is_ident(from_expr):
            if is_ident(to_expr):
                raise BadScriptException('Unknown variable')
            if from_expr.Ident().getText() != v_name:
                raise BadScriptException('Unknown from variable')
            if to_expr.Underscore() is not None:
                return len(s_acceptable) > 0
            if to_expr.Kw_id() is not None:
                return int(to_expr.Int().getText()) in [snd for fst, snd in s_acceptable]
            if to_expr.Kw_random() is not None:
                v = random.randint(0, graph_vertices_amount - 1)
                return v in [snd for fst, snd in s_acceptable]
        # to_expr equals v
        if to_expr.Ident().getText() != v_name:
            raise BadScriptException('Unknown variable')
        if from_expr.Underscore() is not None:
            return len(s_acceptable) > 0
        if from_expr.Kw_id() is not None:
            return int(from_expr.Int().getText()) in [fst for fst, snd in s_acceptable]
        if from_expr.Kw_random() is not None:
            v = random.randint(0, graph_vertices_amount - 1)
            return v in [fst for fst, snd in s_acceptable]


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

    visitor = queryVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
