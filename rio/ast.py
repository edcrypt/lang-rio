"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

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
