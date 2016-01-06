"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

from rio import bytecode


class Node(object):
    """ A node on the Abstract Syntax Tree
    """
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def compile(self, ctx):
        return NotImplemented

class Block(Node):
    """ A list of statements
    """
    def __init__(self, exprs):
        self.exprs = exprs

    def __repr__(self):
        return 'Block({})'.format(self.exprs)

    def compile(self, ctx):
        """ Compile each statement in the block.
        """
        for expr in self.expr:
            expr.compile(ctx)

class Expr(Node):
    """ An expression (a message chain).
    """
    def __init__(self, msgchain):
        self.msgchain = msgchain

    def __repr__(self):
        return 'Expr({})'.format(self.msgchain)

    def compile(self, ctx):
        for msg in self.msgchain[:-1]:
            msg.compile(ctx)
        self.msgchain[-1].compile(ctx, last=True)
        # emit SEND_MSG?
        ctx.emit(bytecode.POP_TOP)

class Message(Node):
    """ Represent a message send.
    """
    def __init__(self, target, args=None):
        # target could be either a literal or a slot
        self.target = target
        self.args = args

    def __repr__(self):
        if self.args:
            return 'Message({}, {})'.format(self.target, self.args)
        return 'Message({})'.format(self.target)

    def compile(self, ctx, last=False):
        self.target.compile(ctx)
        if self.args:
            self.args.compile(ctx)
        if last:
            if self.args:
                return ctx.emit(bytecode.BUILD_MSGWARGS) # len...
            ctx.emit(bytecode.BUILD_MSGCHAIN) # len...


class Args(Node):
    """ An argument list of a message.
    """
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return 'Args({})'.format(self.values)

    def compile(self, ctx):
        pass # emit BUILD_TUPLE len(values)

# TERMINALS

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
