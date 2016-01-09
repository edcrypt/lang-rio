Rio
===

Tutorial
--------

Math
~~~~

Basic arithmetic is supported.

Expressions involving operators get "shuffled", or normalized, to their canonical **message send** form.

::

   1+1
   -> 2

   # checking the 'canonical' form using 'quoting
   '(1+1)
   -> 1 +(1)

   2 sqrt
   -> 1.414214

Variables
~~~~~~~~~

The `=` operator creates attributes. By default, it creates it on the `Core` object.

As the operator purpose is to have a simple "side effect", it returns `None`.

::

   a = 1

   a
   -> 1

   b = 2 * 3

   a + b
   -> 7


Conditions
~~~~~~~~~~

::

   a = 2

   (a == 1) if_true("a is one" print) if_false("a is not one" print)
   -> a is not one


Tables
~~~~~~

Tables are colletions of objects. Each item is composed of a positional *index* starting from 0,
an optional *key* (any immutable object - tuples, text, numbers), and a *value*.
Indexes and keys are used to locate values in the table.

There are two representations for the table: one using *[]*, denoting a table without keys, and
one using *{}*, denoting a table with both indexes and keys.

::

   t = [1, 2, 3]

   t
   -> [1, 2, 3]

   t[0]
   -> 1

   t len
   -> 3

   t["name"] = "value"

   t
   -> {0: 1, 1: 1, 2: 3, "name": "value"}

   t[4] is t["name"]
   -> True

   t any(> 2)
   -> True

Text
~~~~

::

   name = "Malcolm Reynolds' Spaceship"

   lines = """ much "text"
   very long
       much lines
   very ünicode"""

   lines[-7]
   -> "ü"

Loops
~~~~~

::

   1..10 each(print(end=" "))
   -> 1 2 3 4 5 6 7 8 9 10
