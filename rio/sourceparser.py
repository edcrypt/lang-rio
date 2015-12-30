"""
"""
import py
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from rio import rio_dir

grammar = py.path.local(rio_dir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)


class Node(object):
    """ A node on the Abstract Syntax Tree
    """
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

class Block(Node):
    """ A list of statements
    """
    def __init__(self, exprs):
        self.exprs = exprs

class Expr(Node):
    """ A single expression
    """
    def __init__(self, expr):
        self.expr = expr

class Message(Node):
    """ Represent a message send.
    """
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

class ConstantInt(Node):
    """ Represent a constant - integer type
    """
    def __init__(self, intval):
        self.intval = intval

class Identifier(Node):
    def __init__(self, varname):
        """ A variable reference.
        """
        self.varname = varname

class Transformer(object):
    """ Transforms AST from the obscure format given to us by the ebnfparser
    to something easier to work with
    """
    def visit_main(self, node):
        return Block([self.visit_expr(exprnode)
                      for exprnode in node.children])

    def visit_block(self, node):
        pass

    def visit_msg(self, node):
        chnode = node.children[0]
        # either symbol or args
        return Message()

    def visit_expr(self, node):
        chnode = node.children[0]
        if chnode.symbol == 'NUMBER':
            return ConstantInt(int(chnode.additional_info))
        # xxx

transformer = Transformer()

def parse(source):
    """ Parse the source code and produce an AST
    """
    return transformer.visit_main(_parse(source))
