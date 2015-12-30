
from rio.sourceparser import (
    parse, Stmt, Block, Message, ConstantInt, Identifier
)

def test_parse_basic():
    assert parse('50') == Block([Stmt(ConstantInt(50))])
    assert parse('1 inc') == Block(
        [Stmt(Message(ConstantInt(1), Message(Identifier('inc'))))]
    )

