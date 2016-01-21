"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""
from __future__ import print_function

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
        for expr in self.exprs:
            expr.compile(ctx)
            ctx.emit(bytecode.POP_TOP)

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
        self.msgchain[-1].compile(ctx, len(self.msgchain))
        ctx.emit(bytecode.SEND_MSG)

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

    def compile(self, ctx, chain=0):
        self.target.compile(ctx)
        if self.args:
            self.args.compile(ctx)
        if chain:
            if self.args:
                ctx.emit(bytecode.BUILD_MSGWARGS, chain)
            ctx.emit(bytecode.BUILD_MSGCHAIN, chain)


class Args(Node):
    """ An argument list of a message.
    """
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return 'Args({})'.format(self.values)

    def compile(self, ctx):
        for val in self.values:
            val.compile(ctx)
        ctx.emit(bytecode.BUILD_TUPLE, len(self.values))


# TERMINALS

class ConstantInt(Node):
    """ Represent a constant - integer type
    """
    def __init__(self, intval):
        self.intval = intval

    def __repr__(self):
        return 'ConstantInt({})'.format(self.intval)

    def compile(self, ctx):
        ctx.emit(bytecode.PUSH_CONST, ctx.register_constant(self.intval))

class Identifier(Node):
    """ Identifier fora slot reference.
    Either an attribure or a method.
    """
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return 'Identifier("{}")'.format(self.varname)

    def compile(self, ctx):
        ctx.emit(bytecode.PUSH_NAME, ctx.register_var(self.varname))
