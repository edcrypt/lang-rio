# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""
from __future__ import print_function

from rio.parser import parse
from rio.ast import (
    Expr, Block, Message, Args, ConstantInt, Identifier
)


def test_parse_basic():
    assert parse('50') == Block([Expr([Message(ConstantInt('50'))])])
    assert parse('1 inc') == Block(
        [Expr([Message(ConstantInt('1')), Message(Identifier('inc'))])]
    )
    assert parse('a') == Block([Expr([Message(Identifier('a'))])])
    assert parse('a b c') == Block(
        [Expr([Message(Identifier('a')),
               Message(Identifier('b')),
               Message(Identifier('c'))])]
    )
    assert parse('a; c') == Block(
        [Expr([Message(Identifier('a')),
               Message(Identifier(';')),
               Message(Identifier('c'))])]
    )
    assert parse('(a)') == parse('a')
    assert parse('(a b)') == parse('a b')
    assert parse('(a b) c') == parse('a b c')
    assert parse('((a b) c d) e') == parse('a b c d e')

def test_parse_args():
    assert parse('_a(b)') == Block(
        [Expr([Message(Identifier('_a'),
                       Args([Expr([Message(Identifier('b'))])]),
                       )]
        )])
    assert parse('a(50)') == Block(
        [Expr([Message(Identifier('a'),
                       Args([Expr([Message(ConstantInt('50'))])]),
                       )]
        )])
    assert parse('5 pow(ç)') == Block(
        [Expr([
            Message(ConstantInt('5')),
            Message(Identifier('pow'),
                    Args([Expr([Message(Identifier('ç'))])]))]
        )])
    assert parse('a(b, c)') == Block(
        [Expr([Message(Identifier('a'), Args(
            [Expr([Message(Identifier('b'))]),
             Expr([Message(Identifier('c'))])]
        ))])]
    )
    assert parse('a(b, (c))') == parse('a(b,c)')
    assert parse('a(b, c)') == parse('a(b,c,)')
    assert parse('a(b, c)') == parse('a(\nb,\nc\n)')
    assert parse('a(b, c)') == parse('a(b,c,\n)')
    assert parse('a(b, c)') == parse('a(\n\nb,\n\nc,\n\n)\n')

def test_parse_blocks():
    assert parse('a b c\nd') == Block([
        Expr([Message(Identifier('a')),
              Message(Identifier('b')),
              Message(Identifier('c'))]),
        Expr([Message(Identifier('d'))]),
    ])
    assert parse('a\nb\nc\nd') == Block([
        Expr([Message(Identifier('a'))]),
        Expr([Message(Identifier('b'))]),
        Expr([Message(Identifier('c'))]),
        Expr([Message(Identifier('d'))]),
    ])
