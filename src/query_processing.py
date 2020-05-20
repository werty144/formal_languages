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
        if ctx.select_stmt() is not None and ctx.Kw_write() is not None:
            out_file = open(ctx.String()[1:-1], 'w')
            res = self.visitSelect_stmt(ctx.select_stmt())
            out_file.write(str(res))
            out_file.close()

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
        s_acceptable, graph = self.get_s_acceptable(ctx)
        vs_info = ctx.obj_expr().vs_info().Ident()
        from_expr = ctx.where_expr().v_expr()[0]
        to_expr = ctx.where_expr().v_expr()[1]
        kwargs = {
            'vs_info': vs_info,
            'from_expr': from_expr,
            'to_expr': to_expr,
            's_acceptable': s_acceptable,
            'graph_vertices_amount': graph.vertices_amount(),
            'graph': graph
        }
        try:
            if ctx.obj_expr().Kw_exists() is not None:
                return self.process_exists(**kwargs)
            if ctx.obj_expr().Kw_count() is not None:
                return self.process_count(**kwargs)
            if ctx.obj_expr().Kw_isolated() is not None:
                return self.process_isolated(**kwargs)
            if ctx.obj_expr().Kw_count_neighbours() is not None:
                return self.process_count_neighbours(**kwargs)
            if ctx.obj_expr().Kw_singular is not None:
                return self.process_singular(**kwargs)
            if ctx.obj_expr().Kw_count_adjacent is not None:
                return self.process_count_adjacent(**kwargs)
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
        return s_acceptable, graph

    @staticmethod
    def process_obj_expr_template(
                                  pair_func,
                                  single_func,
                                  **kwargs
    ):
        vs_info = kwargs['vs_info']
        from_expr = kwargs['from_expr']
        to_expr = kwargs['to_expr']
        s_acceptable = kwargs['s_acceptable']
        graph_vertices_amount = kwargs['graph_vertices_amount']
        if len(vs_info) == 2:
            if not (is_ident(from_expr) and is_ident(to_expr)):
                raise BadScriptException('Condition on fix variable')
            return pair_func(s_acceptable)
        # if one variable
        v_name = vs_info[0].getText()
        if is_ident(from_expr):
            if is_ident(to_expr):
                raise BadScriptException('Unknown variable')
            if from_expr.Ident().getText() != v_name:
                raise BadScriptException('Unknown from variable')
            if to_expr.Underscore() is not None:
                vertices = [fst for fst, snd in s_acceptable]
                return single_func(vertices)
            if to_expr.Kw_id() is not None:
                vertices = list(filter(lambda p: p[1] == int(kwargs['to_expr'].Int().getText()), s_acceptable))
                return single_func(vertices)
            if to_expr.Kw_random() is not None:
                u = random.randint(0, graph_vertices_amount - 1)
                vertices = list(filter(lambda p: p[1] == u, kwargs['s_acceptable']))
                return single_func(vertices)
        # to_expr equals v
        if to_expr.Ident().getText() != v_name:
            raise BadScriptException('Unknown variable')
        if from_expr.Underscore() is not None:
            vertices = [snd for fst, snd in s_acceptable]
            return single_func(vertices)
        if from_expr.Kw_id() is not None:
            vertices = list(filter(lambda p: p[0] == int(kwargs['from_expr'].Int().getText()), s_acceptable))
            return single_func(vertices)
        if from_expr.Kw_random() is not None:
            u = random.randint(0, graph_vertices_amount - 1)
            vertices = list(filter(lambda p: p[0] == u, kwargs['s_acceptable']))
            return single_func(vertices)

    def process_exists(self, **kwargs):
        def pair_func(pairs):
            return len(pairs) > 0

        def exists(vertices):
            return len(vertices) > 0

        return self.process_obj_expr_template(pair_func, exists, **kwargs)

    def process_count(self, **kwargs):
        def pair_func(pairs):
            return len(pairs)

        def count(vertices):
            return len(set(vertices))

        return self.process_obj_expr_template(pair_func, count, **kwargs)

    def process_isolated(self, **kwargs):
        def pair_func(pairs):
            raise BadScriptException('Isolated expr is not for pairs!')

        def isolated(vertices):
            import itertools
            graph = kwargs['graph']
            for u, v in itertools.product(vertices):
                if graph.connected(u, v):
                    return False
            return True

        return self.process_obj_expr_template(pair_func, isolated, **kwargs)
    
    def process_count_neighbours(self, **kwargs):
        def pair_func(pairs):
            raise BadScriptException('Count neighbours is not for pairs!')

        def count_neighbors(vertices):
            graph = kwargs['graph']
            return len(set([item for sublist in [graph.get_neighbours(v) for v in vertices] for item in sublist]))

        return self.process_obj_expr_template(pair_func, count_neighbors, **kwargs)

    def process_singular(self, **kwargs):
        def pair_func(pairs):
            return len(pairs) == 1

        def singular(vertices):
            return len(vertices) == 1

        return self.process_obj_expr_template(pair_func, singular, **kwargs)

    def process_count_adjacent(self, **kwargs):
        def pair_func(pairs):
            graph = kwargs['graph']
            return len(list(filter(lambda p: graph.adjacent(p[0], p[1]), pairs)))

        def count_adjacent(vertices):
            raise BadScriptException('Count adjacent is not for single vertex!')

        return self.process_obj_expr_template(pair_func, count_adjacent, **kwargs)


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
