lang-rio
========

Learning how to build an interpreter with Pypy's RPython.

Goal: a JIT-compiled interpreter for a simple Io_-inspired
OOPL, only a bit more pythonic in style and favored idioms.

See goals.org_ file for design goals, ideas and progress.

See the tutorial_ file for an outline of what it should look like.

To check the parser and the compiler working::

  pip install -r requirements
  pip install http://www.pygame.org/ftp/pygame-1.9.1release.tar.gz
  python -m rio.parser "a b c(d); 50" --draw
  python -m rio.bytecode "a b c"


References
==========

* `Getting Started`_ with Pypy development

* `Coding Guide`_

* Kermit example interpreter:

  - original: https://bitbucket.org/pypy/example-interpreter
  - fork: https://github.com/prologic/kermit / https://github.com/edcrypt/kermit

* `Pypy Tutorial - BF`_
* `EBNF`_

* Other interpreters:

  - lang-io: https://bitbucket.org/pypy/lang-io/
  - CyCy: https://media.readthedocs.org/pdf/building-an-interpreter-with-rpython/latest/building-an-interpreter-with-rpython.pdf
  - Pypy.js: http://pypyjs.org/
  - Prolog on Pypy: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.103.1886&rep=rep1&type=pdf
  - Smalltalk: `Implementing a SM VM in Pypy in 1w`_ / `RSqueak`_
  - Pixie (lisp): https://github.com/pixie-lang/pixie

* On bytecode generation:

  - `All Singing All Dancing Python Bytecode`_
  - `Maynard`_
  - `Byterun`_

.. _All Singing All Dancing Python Bytecode: https://www.youtube.com/watch?v=0IzXcjHs-P8#t=36s
.. _Byterun: https://github.com/nedbat/byterun
.. _Maynard: https://bitbucket.org/larry/maynard
.. _goals.org: ./docs/goals.org
.. _tutorial: ./docs/tutorial.rst
.. _Io: http://iolanguage.org
.. _Getting Started:  http://doc.pypy.org/en/latest/getting-started-dev.html
.. _Coding Guide: http://doc.pypy.org/en/latest/coding-guide.html
.. _Pypy Tutorial - BF: https://bitbucket.org/brownan/pypy-tutorial/
.. _EBNF: http://doc.pypy.org/en/release-1.9/rlib.html#ebnf
.. _Implementing a SM VM in Pypy in 1w: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.144.8184&rep=rep1&type=pdf
.. _RSqueak: https://github.com/HPI-SWA-Lab/RSqueak
