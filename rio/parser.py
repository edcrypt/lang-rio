"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

import py
from rpython.rlib.parsing.tree import RPythonVisitor
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function

from rio import RIO_DIR
from rio.ast import (
    Expr, Block, Message, Args, ConstantInt, Identifier
)


class Transformer(RPythonVisitor):
    """ Transforms an AST from the format given to us by the ebnfparser
    to something easier to work with.
    """
    debug = False
    def visit_main(self, node):
        # a program is a single block of code
        if self.debug:
            node.view()
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


class RioParser(object):
    """ Uses a grammar file to generate an AST for some source code in RIO.
    """
    def __init__(self, grammar_dir=RIO_DIR,
                 grammar_filename='grammar.ebnf',
                 TransformerKlass=Transformer,
                 *targs, **tkw):
        self.grammar = py.path.local(
           grammar_dir).join(grammar_filename).read("rt")
        self.transformer = TransformerKlass(*targs, **tkw)
        self._make_parse_function()

    def _make_parse_function(self):
        regexs, rules, ToAST = parse_ebnf(self.grammar)
        self._clean_tree = ToAST().transform
        self._parse = make_parse_function(regexs, rules, eof=True)

    def gen_ast(self, source):
        tree_from_enbf = self._parse(source)
        cleaned_tree = self._clean_tree(tree_from_enbf)
        return self.transformer.dispatch(cleaned_tree)

    def debug_mode(self):
        """Draw a pretty graph of the parsed AST
        """
        self.transformer.debug = True

_rio_parser = RioParser()

def parse(source, debug=False):
    """ Parse the source code and produce an AST
    """
    return _rio_parser.gen_ast(source)

if __name__ == '__main__':
    import sys
    from ipdb import launch_ipdb_on_exception

    if '--draw' in sys.argv:
        _rio_parser.debug_mode()
    try:
        source = py.path.local(sys.argv[1], expanduser=True).read('rt')
    except IndexError:
        print 'python -m rio.parser file_or_code [--draw]'
        sys.exit(1)
    except py.error.ENOENT:
        source = sys.argv[1]
    with launch_ipdb_on_exception():
        print parse(source)
