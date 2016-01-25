# -*- coding: utf-8 -*-
"""
Rio PL interpreter
------------------

Rio Objects
~~~~~~~~~~~

Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

# Here we define our basic object hierarchy.
# Most methods will have to be defined in terms of
# 'primitive' operations, registered using a decorator.



class W_Object(object):
    """ Rio object tree root.
    """
    pass


class W_Number(W_Object):
    pass


class W_Integer(W_Number):
    pass


# TODO: Iterable, Sequence, Text, Table, Range, Float, Block, Message, Method

