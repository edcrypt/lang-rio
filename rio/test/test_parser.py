
from rio.sourceparser import (
    parse, Expr, Block, Message, ConstantInt, Identifier
)

def test_parse_basic():
    assert parse('50') == Block([Expr([Message(ConstantInt('50'))])])
    assert parse('1 inc') == Block(
        [Expr([Message(ConstantInt('1')), Message(Identifier('inc'))])]
    )

