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

import py

from rio.bytecode import Bytecode, RETURN_VALUE


class CompilerContext(object):
    def __init__(self):
        self.data = []
        self.constants = []
        self._names = []
        self._names_to_numbers = {}

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def register_var(self, name):
        try:
            return self._names_to_numbers[name]
        except KeyError:
            self._names_to_numbers[name] = len(self._names)
            self._names.append(name)
            return len(self._names) - 1

    def emit(self, bytecode, arg=0):
        self.data.append(chr(bytecode))
        self.data.append(chr(arg))

    def create_bytecode(self):
        return Bytecode("".join(self.data), self.constants[:], len(self._names))


def compile_ast(astnode):
    c = CompilerContext()
    astnode.compile(c)
    c.emit(RETURN_VALUE, 0)
    return c.create_bytecode()


if __name__ == '__main__':
    import sys
    from rio.parser import parse, RioSyntaxError

    try:
        source = py.path.local(sys.argv[1], expanduser=True).read('rt')
    except IndexError:
        print('python -m rio.bytecode file_or_code')
        sys.exit(1)
    except py.error.ENOENT:
        source = sys.argv[1]
    try:
        print(compile_ast(parse(source)))
    except RioSyntaxError:
        sys.exit(1)
