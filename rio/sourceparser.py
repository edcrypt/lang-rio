"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

import py
from rpython.rlib.parsing.tree import RPythonVisitor
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function

from rio import rio_dir
from rio.ast import (
    Expr, Block, Message, Args, ConstantInt, Identifier
)


grammar = py.path.local(rio_dir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)


class Transformer(RPythonVisitor):
    """ Transforms AST from the obscure format given to us by the ebnfparser
    to something easier to work with
    """
    def visit_main(self, node):
        # a program is a single block of code
        return self.dispatch(node.children[0])

    def visit_block(self, node):
        # a block is built of multiple expressions
        return Block([self.dispatch(exprnode)
                      for exprnode in node.children])

    def visit_expr(self, node):
        # every expression is a message chain
        return Expr([self.dispatch(child)
                     for child in node.children])

    def visit_message(self, node):
        # a message (fragment) is a symbol and maybe some args
        target = self.dispatch(node.children[0])
        if len(node.children) > 1 and node.children[1].children:
            args = self.dispatch(node.children[1])
            return Message(target, args)
        return Message(target)

    def visit_arguments(self, node):
        return Args([self.dispatch(child)
                     for child in node.children])

    # LITERALS/SYMBOLS
    def visit_NUMBER(self, node):
        return ConstantInt(node.additional_info)

    def visit_IDENTIFIER(self, node):
        return Identifier(node.additional_info)


transformer = Transformer()

def parse(source):
    """ Parse the source code and produce an AST
    """
    tree = _parse(source)
    tree = ToAST().transform(tree)
    return transformer.dispatch(tree)
