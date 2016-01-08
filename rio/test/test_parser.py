# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

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

def test_parse_no_args():
    # Yes, we don't have Python's distinction between getting an attrib
    # and calling a method. But you should be able to 'quote a message.
    # Also, we can use get_slot
    assert parse('a') == Block([Expr([Message(Identifier('a'))])])
    assert parse('a;') == parse('a')
    assert parse('a()') == Block([Expr([Message(Identifier('a'))])])
    assert parse('a()') == parse('a;')
    assert parse('a\n') == Block([Expr([Message(Identifier('a'))])])
    assert parse('a\n') == parse('a()')
    assert parse('a;\n') == parse('a')
    assert parse('a()\n') == parse('a')
    assert parse('a b()') == Block(
        [Expr([Message(Identifier('a')),
               Message(Identifier('b'))])])
    assert parse('a b() c') == Block(
        [Expr([Message(Identifier('a')),
               Message(Identifier('b')),
               Message(Identifier('c'))])])
    assert parse('a b() c') == parse('a b(\n) c')

def test_parse_args():
    assert parse('a(b)') == Block(
        [Expr([Message(Identifier('a'),
                       Args([Expr([Message(Identifier('b'))])]),
                       )]
        )])
    assert parse('a(50)') == Block(
        [Expr([Message(Identifier('a'),
                       Args([Expr([Message(ConstantInt('50'))])]),
                       )]
        )])
    assert parse('5 pow(c)') == Block(
        [Expr([
            Message(ConstantInt('5')),
            Message(Identifier('pow'),
                    Args([Expr([Message(Identifier('c'))])]))]
        )])
    assert parse('a(b, c)') == Block(
        [Expr([Message(Identifier('a'), Args(
            [Expr([Message(Identifier('b'))]),
             Expr([Message(Identifier('c'))])]
        ))])]
    )
    assert parse('a(b, c)') == parse('a(\nb,\nc\n)')
    assert parse('a(b, c)') == parse('a(b,c,)')
    assert parse('a(b, c)') == parse('a(b,c,\n)')
    assert parse('a(b, c)') == parse('a(\n\nb,\n\nc,\n\n)\n')


def test_parse_blocks():
    assert parse('a b c\nd') == Block([
        Expr([Message(Identifier('a')),
              Message(Identifier('b')),
              Message(Identifier('c'))]),
        Expr([Message(Identifier('d'))]),
    ])
    assert parse('a b c; d') == Block([
        Expr([Message(Identifier('a')),
              Message(Identifier('b')),
              Message(Identifier('c'))]),
        Expr([Message(Identifier('d'))]),
    ])
    assert parse('a;b;c') == parse('a\nb\nc # ";" is equivalent to \\n')
    assert parse('a;b;\nc') == parse('a\n\nb\nc')
    assert parse('a;b;c') == parse('a\nb\n\nc\n')
    assert parse('a;b;c') == parse('a\n\n\n\nb\n\n\nc')
    assert parse('a;b b1;c') == parse('a\nb b1\nc\n#this is a comment, alone')
    assert parse('a;\nb b1;c') == parse('a\nb b1;\n\nc')
    assert parse('a\nb b1;c') == parse('a\nb b1;\n\nc')
    assert parse('a\nb b1;c') == parse('a\nb b1\t;\n\nc;')
    assert parse('a\nb b1;c') == parse('a\nb b1\f;\n\nc;\n\n')
    assert parse('1;a;b') == Block([
        Expr([Message(ConstantInt('1'))]),
        Expr([Message(Identifier('a'))]),
        Expr([Message(Identifier('b'))]),
    ])
    assert parse(' a ; b ') == parse('a;b')