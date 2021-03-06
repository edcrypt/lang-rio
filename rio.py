"""
Rio PL interpreter
------------------


Author: Eduardo de Oliveira Padoan
Email:  eduardo.padoan@gmail.com
"""

import os
import sys

from rpython.rlib.parsing.ebnfparse import parse_ebnf



# GOAL SYNTAX
##############
# exp        ::= { message | terminator }
# message    ::= symbol [arguments]
# arguments  ::= "(" [exp [ { "," exp } ]] ")"
# symbol     ::= identifier | number | string
# terminator ::= "\n" | ";"
##############
# (From the iolang docs. Note that it doesn't include algebraic exprs)
# See rio/grammar.txt for progress

SYNTAX = ""

def parse(program):
    rs, rules, transformer = parse_ebnf(SYNTAX)
    # ...
    bm = None
    return program, bm


def mainloop(program, bm):
    pass


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    program, bm = parse(program_contents)
    mainloop(program, bm)


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        # TODO: enter REPL
        print "You must supply a filename"
        return 1
    import ipdb; ipdb.set_trace()
    try:
        run(os.open(filename, os.O_RDONLY, 0777))
    except OSError:
        print "File not found:", filename
    return 0


def target(*args):
    return entry_point, None


def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()


if __name__ == "__main__":
    # env PYTHONPATH=../pypy python rio.py test.rio
    entry_point(sys.argv)