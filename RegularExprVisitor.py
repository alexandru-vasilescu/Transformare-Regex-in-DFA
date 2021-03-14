# Generated from RegularExpr.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RegularExprParser import RegularExprParser
else:
    from RegularExprParser import RegularExprParser

# This class defines a complete generic visitor for a parse tree produced by RegularExprParser.

class RegularExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RegularExprParser#expr.
    def visitExpr(self, ctx:RegularExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegularExprParser#c_expr.
    def visitC_expr(self, ctx:RegularExprParser.C_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegularExprParser#s_expr.
    def visitS_expr(self, ctx:RegularExprParser.S_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegularExprParser#atom.
    def visitAtom(self, ctx:RegularExprParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegularExprParser#variabila.
    def visitVariabila(self, ctx:RegularExprParser.VariabilaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegularExprParser#inner_expr.
    def visitInner_expr(self, ctx:RegularExprParser.Inner_exprContext):
        return self.visitChildren(ctx)



del RegularExprParser