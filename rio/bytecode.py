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
xkPUSH_CONST       4 (50)
BUILD_TUPLE      3
SEND_MSGWARGS    2

Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""



bytecodes = [
    'PUSH_NAME',     # Push name #N from context to the stack

    'PUSH_CONST',    # Push constant #N from context to the stack

    'BUILD_TUPLE',   # Build tuple with N itens
                     # Remove items from stack, add tuple back

    'SEND_MSGCHAIN', # Build simple message chain from N items
                     # Remove items from stack, add msg result back

    'SEND_MSGWARGS', # Build message chain from N items (except top of stack)
                     # Plus top of stack as args tuple
                     # Remove top + N items from stack, add msg result back

    'POP_TOP',       # Remove top of the stack
]

