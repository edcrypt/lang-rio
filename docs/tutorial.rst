Rio
===

Tutorial
--------

Notation: in this tutorial, **=>** indicates the result of a previos expression, and **->** indicates
a print to the standard output.


Math
~~~~

Basic arithmetic is supported.

Expressions involving operators get "shuffled", or normalized, to their canonical **message send** form.

::

   1+1
   => 2

   # checking the 'canonical' form using 'quoting
   '(1+1)
   => 1 +(1)

   2 sqrt
   => 1.414214

Variables
~~~~~~~~~

The `=` operator creates attributes. By default, it creates it on the `Core` object.

As the operator exclusive purpose is to have a "side effect", it returns `None`.

::

   a = 1

   a
   => 1

   b = 2 * 3

   a + b
   => 7


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
   => [1, 2, 3]

   t any(> 2)
   => True

   t[0]
   => 1

   t len
   => 3

   t["name"] = "value"

   t
   => {0: 1, 1: 1, 2: 3, "name": "value"}

   t[4] is t["name"]
   => True

   # a 'Mapping' object
   1:2
   -> 1:2


   # tables can be created from mappings
   t2 = {"a": "b", ¨c": "d"}

   # dict and list are Core methods that create Tables
   # with and without keys from other iterables
   list(1..10)
   => [1, 2, 3, 4, 5, 6, 7, 8, 9]

   dict((1:2, 2:3))
   => {1: 2, 2: 3}

Text
~~~~

::

   name = "Malcolm Reynolds' Spaceship"

   lines = """ much "text"
   very long
       much lines
   very ünicode"""

   lines[-7]
   => "ü"

Loops
~~~~~

::

   # send the message "print" to each item produced by the Range object
   # also, "keyword" arguments are passed using mappings
   1..10 each(print(end: " "))
   -> 1 2 3 4 5 6 7 8 9 10

   # longer form -- uses pattern matching to dispatch to the right implementation
   1..10 each(num,
       num print(end: " ")
   )
   -> 1 2 3 4 5 6 7 8 9 10

   help(Range each)
   -> Range each('msg)
   ->     Send `msg` to each item produced.
   -> Range each('name, 'msg)
   ->     For each item, send `msg`, with `name` in the local namespace as the current item.

   found = False

   # "while_true" is a method of Message
   # it evaluates a copy of the message each time
   '(not found) while_true(
       found = search()
   )

Objects
~~~~~~~

::

   Contact = Object clone

   Contact proto
   => Object

   Contact name = None
   Contact email = None

   # _ to avoid external access
   Contact _description = None
   Contact _summary_template = """
   Name: {}
   Email: {}
   {}
   """

   Contact dir
   => {"name": None, "email": None}

   # Before we start defining methods, let's check the docs
   help(method)
   -> Core method(*args, 'code)
   ->     Create a `Method` object.
   ->     - `args`: the arguments defining the pattern to be matched at message send time.
   ->     - `code`: the expressions that are executed when the message associated with this
   ->               method is received.

   Contact describe = method(
       self _summary_templ format(self name, self email, self _description) print
   )

   Contact describe_as = method(new_descr,
       "Updates the contact description"
       self _history append(self _description)
       self _description = new_descr
   )

   Contact getattr("describe_as") doc
   => "Updates the contact description"

   help(Contact describe_as)
   -> Contact describe_as(new_descr)
   ->     Updates the contact description

   Contact init = method(name, email, description,
       self name = name
       self email = email
       self _description = description
       self _history = []
   )

   alex = Contact clone("Alex", "alex@example.com", "A good person")

