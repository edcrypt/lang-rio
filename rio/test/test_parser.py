
from rio.sourceparser import (
    parse, Expr, Block, Message, ConstantInt, Identifier
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

def test_parse_args():
    pass

def test_parse_blocks():
    pass

