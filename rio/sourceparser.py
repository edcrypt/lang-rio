"""
"""
import py
from rpython.rlib.parsing.tree import RPythonVisitor
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

    def __repr__(self):
        return 'Block({})'.format(self.exprs)

class Expr(Node):
    """ An expression (a message chain).
    """
    def __init__(self, msgchain):
        self.msgchain = msgchain

    def __repr__(self):
        return 'Expr({})'.format(self.msgchain)

class Message(Node):
    """ Represent a message send.
    """
    def __init__(self, target, args=None):
        # target could be either a literal or a slot
        self.target = target
        self.args = args

    def __repr__(self):
        if self.args is None:
            return 'Message({})'.format(self.target)
        return 'Message({}, {})'.format(self.target, self.args)

class ConstantInt(Node):
    """ Represent a constant - integer type
    """
    def __init__(self, intval):
        self.intval = intval

    def __repr__(self):
        return 'ConstantInt({})'.format(self.intval)

class Identifier(Node):
    """ Identifier fora slot reference.
    Either an attribure or a method.
    """
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return 'Identifier("{}")'.format(self.varname)

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
        args = (self.dispatch(node.children[1])
                if len(node.children) > 1 else None)
        return Message(target, args)

    def visit_argument(self, node):
        pass

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
