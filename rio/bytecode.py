# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------

AST to Bytecode compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ex.:
>> 'a b = 50
=> Core =(a, b, 50)
>> dis('a b = 50) print
PUSH_NAME        0 (Core)
PUSH_NAME        1 (=)
PUSH_NAME        2 (a)
PUSH_NAME        3 (b)
PUSH_CONST       0 (50)
BUILD_TUPLE      3
BUILD_MSGWARGS   2

Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""
from __future__ import print_function


BYTECODES = [
    ### Compile-time emitted bytecodes
    'POP_TOP',        # Remove top of the stack (TOS)

    'PUSH_NAME',      # Push name #N from context to the stack

    'PUSH_CONST',     # Push constant #N from context to the stack

    'BUILD_TUPLE',    # Build tuple with N itens
                      # Remove items from stack, add tuple back

    'BUILD_MSGCHAIN', # Build simple message chain from N items
                      # Remove items from stack, add msg obj back

    'BUILD_MSGWARGS', # Build message chain from N items (except top of stack)
                      # Plus top of stack as args tuple
                      # Remove top + N items from stack, add msg obj back

    'SEND_MSG',       # Remove TOS, exec it and add msg result back in the stack

    'RETURN_VALUE',   # End current block with TOS as message return value

    ### Bytecode emitted by 'primitive' methods
    #   Control flow
    'JUMP_IF_FALSE',  # Jump forwards in the bytecode counter of TOS is False
                      # Also add this point to a 'marks ring' on the context

    'JUMP_BACKWARDS', # Jump back to the latest mark on the ring

    #   Algebra
    'BINARY_ADD',
    # TODO...
]


for i, bytecode in enumerate(BYTECODES):
    globals()[bytecode] = i


class CompilerContext(object):
    def __init__(self):
        self.data = []
        self.constants = []
        self._names = []
        self._names_to_numbers = []

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def register_var(self, name):
        try:
            return self._names_to_numbers[name]
        except KeyError:
            self.names_to_numbers[name] = len(self._names)
            self._names.append(name)
            return len(self._names) - 1

    def emit(self, bytecode, arg=0):
        self.data.append(chr(bytecode))
        self.data.append(chr(arg))

    def create_bytecode(self):
        return Bytecode("".join(self.data), self.constants[:], len(self._names))


class Bytecode(object):
    def __init__(self, code, constants, numvars):
        self.code = code
        self.constants = constants
        self.numvars = numvars

    def dump(self):
        lines = []
        i = 0
        for i in range(0, len(self.code), 2):
            c = self.code[i]
            c2 = self.code[1 + 1]
            lines.append(BYTECODES[ord(c)] + " " + str(ord(c2)))
        return '\n'.join(lines)


def compile_ast(astnode):
    c = CompilerContext()
    astnode.compile(c)
    c.emit(RETURN_VALUE, 0)
    return c.create_bytecode()