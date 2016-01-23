# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""
from __future__ import print_function

from rio.parser import parse
from rio.bytecode import compile_ast

class TestCompiler(object):
    def check_compile(self, source, expected):
        bc = compile_ast(parse(source))
        assert [i.strip()
                for i in expected.splitlines()
                if i.strip()] == bc.dump().splitlines()

    def test_basic(self):
        self.check_compile("1", '''
        PUSH_CONST 0
        BUILD_MSGCHAIN 1
        SEND_MSG 0
        POP_TOP 0
        RETURN_VALUE 0
        ''')

    def test_add(self):
        self.check_compile('a b(1)', '''
        PUSH_NAME 0
        PUSH_NAME 1
        PUSH_CONST 0
        BUILD_MSGCHAIN 1
        SEND_MSG 0
        BUILD_TUPLE 1
        BUILD_MSGWARGS 2
        SEND_MSG 0
        POP_TOP 0
        RETURN_VALUE 0
        ''')

