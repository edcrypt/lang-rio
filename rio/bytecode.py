# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------

Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

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
            c2 = self.code[i + 1]
            lines.append(BYTECODES[ord(c)] + " " + str(ord(c2)))
        return '\n'.join(lines)

    def __repr__(self):
        return self.dump()
