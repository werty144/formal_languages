# Generated from /home/user/PycharmProjects/formal_languages/query_languages/graph_query_grammar.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .graph_query_grammarParser import graph_query_grammarParser
else:
    from graph_query_grammarParser import graph_query_grammarParser

# This class defines a complete generic visitor for a parse tree produced by graph_query_grammarParser.

class graph_query_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by graph_query_grammarParser#script.
    def visitScript(self, ctx:graph_query_grammarParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#stmt.
    def visitStmt(self, ctx:graph_query_grammarParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#named_pattern.
    def visitNamed_pattern(self, ctx:graph_query_grammarParser.Named_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#select_stmt.
    def visitSelect_stmt(self, ctx:graph_query_grammarParser.Select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#obj_expr.
    def visitObj_expr(self, ctx:graph_query_grammarParser.Obj_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#vs_info.
    def visitVs_info(self, ctx:graph_query_grammarParser.Vs_infoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#where_expr.
    def visitWhere_expr(self, ctx:graph_query_grammarParser.Where_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#v_expr.
    def visitV_expr(self, ctx:graph_query_grammarParser.V_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#pattern.
    def visitPattern(self, ctx:graph_query_grammarParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#alt_elem.
    def visitAlt_elem(self, ctx:graph_query_grammarParser.Alt_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#seq.
    def visitSeq(self, ctx:graph_query_grammarParser.SeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#seq_elem.
    def visitSeq_elem(self, ctx:graph_query_grammarParser.Seq_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by graph_query_grammarParser#prim_pattern.
    def visitPrim_pattern(self, ctx:graph_query_grammarParser.Prim_patternContext):
        return self.visitChildren(ctx)



del graph_query_grammarParser