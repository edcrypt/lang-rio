Rio
===

Tutorial
--------

Notation
    In this tutorial, ``=>`` indicates the result of a previous expression, and ``->`` indicates
    a print to the standard output.

Math
~~~~

Basic arithmetic is supported.

Expressions involving operators get "shuffled", or normalized, to their canonical **message send** form::

   1+1
   => 2

   # checking the "canonical" form using 'quoting
   '(1+1)
   => 1 +(1)

   2 sqrt
   => 1.414214

   # Ignore the evaluation of the expression before ";"
   2-1; 2*3
   => 6

Variables
~~~~~~~~~

The ``=`` operator creates attributes. By default, it creates them on the ``Core`` object.

As the operator exclusive purpose is to have a "side effect", the return is ``None``.

::

   a = 1

   a
   => 1

   b = 2 * 3

   c = a + b

   c
   => 7


Conditions
~~~~~~~~~~

Conditional control flow is done with ``Object if_true`` and ``Object if_false``.
There is also a ternary operator form with ``Core ?!``::

   a = 2

   (a == 1) if_true("a is one" print) if_false("a is not one" print)
   -> a is not one

   0 ? "0's boolean value is true!" ! "0 (and empty sequences) has a false boolean value"
   => "0 (and empty sequences) has a false boolean value"

   # A little introspection
   help(Core ?!)
   -> Core ?!(condition, 'do_if_true, 'do_if_false)
   ->     Evaluate 'do_if_true when the condition boolean value is true,
   ->     'do_if_false otherwise.

Tuples
~~~~~~


::

   (1, 2)

   a, b = 1, 2


Tables
~~~~~~

Tables are colletions of objects. Each item is composed of a positional *index* starting from 0,
an optional *key* (any immutable object - tuples, text, numbers), and a *value*.
Indexes and keys are used to locate values in the table.

There are two representations for the table: one using ``[]``, denoting a table without keys, and
one using ``{}``, denoting a table with both indexes and keys::

   t = [1, 2, 3]

   t
   => [1, 2, 3]

   # A list is also an Iterable, so it has some useful methods
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
   => 1:2

   '(a:0)
   => :(a, 0)

   help(Core :)
   -> Core :('key, value)
   ->     Create a Mapping, a simple key:value pair.

   # keys are lazyly evaluated
   a, b = 1, 2
   m = a:b
   m
   => a:2

   m eval_key
   => 1:2

   # Tables can be created from mappings between {}
   t2 = {a: "a", b: "b"}

   t2 eval_keys
   => {1: "a", 2: "b"}

   # "dict" and "list" are shortcut Core methods that create Tables with and
   # without keys, from other iterables
   list(1..10)
   => [1, 2, 3, 4, 5, 6, 7, 8, 9]

   dict((1:2, 2:3))
   => {1: 2, 2: 3}


Text
~~~~

::

   name = "malcolm reynolds' spaceship"

   name title
   => "Malcolm Reynolds' Spaceship"

   lines = """ much "text"
   very long
       much lines
   very ünicode"""

   # Text is a sequence of... Text.
   lines[-7]
   => "ü"


Loops
~~~~~


The methods ``Message while_true`` and ``Iterable each`` provide ways to repeat an expression::

   found = False

   numbers = [1, 3, 6] iter
   # search a number divisible by 2
   '(not found) while_true(
       i = numbers next
       found = not i % 2
   )

   # Send the message "print" to each item produced by the Range object
   # Also, "keyword" arguments are passed using mappings from names to values
   1..10 each(print(end: " "))
   -> 1 2 3 4 5 6 7 8 9 10

   # Longer form -- uses pattern matching to dispatch to the right implementation
   1..10 each(num,
       num print(end: " ")
   )
   -> 1 2 3 4 5 6 7 8 9 10

   help(Range each)
   -> Range each('msg)
   ->     Send `msg` to each item produced.
   -> Range each('name, 'msg)
   ->     For each item, send `msg`, with `name` in the local namespace as the current item.


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
   -> Core method(*args, doc: "", 'code)
   ->     Create a `Method` object.
   ->     - `args`: The arguments defining the pattern to be matched at message send time.
   ->               Check help(ARGSSPEC) for star-arguments, default values and lazy arguments.
   ->     - `doc`:  A text documenting the method.
   ->     - `code`: The message chain executed when the message associated with this
   ->               method is received.

   # yes, *args (star-arguments) is a Message object, and * works as a prefix operator:
   # it works similar to quoting, but indicates multiple arguments.
   '(*args)
   -> *(args)

   # this method will return None: the last -- in this case, only -- expression is returned
   Contact describe = method(
       self _summary_templ format(self name, self email, self _description) print
   )

   Contact describe_as = method(new_descr,
       "Updates the contact description",
       # The following is a single expression.
       # Note that we dont need ";", as None delegates to Core
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

   alex = Contact clone("Alex", "alec@example.com", "A good person")

   alex describe
   -> Name: Alex
   -> Email: alec@example.com
   -> A good person

   # Ops, we misspeled their email!
   alex email = "alex@example.com"

   # Also, we change our views on Alex.
   alex describe_as("Somebody that we used to know.")

   Acquaintance = Object clone

   Acquaintance how_we_met = property(
       self history["how_we_met"]
   )

   Acquaintance how_we_met setter(value,
       self history["how_we_met"] = value
   )

   alex append_proto(Acquaintance)

   alex how_we_met = "At a convention"
