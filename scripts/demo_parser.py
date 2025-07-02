#!/usr/bin/env python3
"""
scripts/demo_parser.py

A tiny REPL that loads grammar/nlang.lark and prints parse trees + AST snippets.
"""

import sys
from lark import Lark, Transformer

# 1) Load the grammar
parser = Lark.open('grammar/nlang.lark', parser='lalr', start='start')

# 2) Define a Transformer to convert the parse tree into a simpler AST
class ASTBuilder(Transformer):
    def __default__(self, data, children, meta):
        return {data: children}

    def let(self, children):      return {"Let": children}
    def define(self, children):   return {"Define": children}
    def set_(self, children):     return {"Set": children}
    def if_(self, children):      return {"If": children}
    def for_(self, children):     return {"For": children}
    def while_(self, children):   return {"While": children}
    def return_(self, children):  return {"Return": children}
    def print_(self, children):   return {"Print": children}
    def import_(self, children):  return {"Import": children}

    def id(self, token):           return {"Identifier": str(token[0])}
    def num(self, token):          return {"Number": float(token[0])}
    def str(self, token):          return {"String": token[0][1:-1]}
    def true(self, _):             return {"Boolean": True}
    def false(self, _):            return {"Boolean": False}

# 3) REPL loop
def repl():
    print("NLang demo parser. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            text = input("nlang> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        txt = text.strip()
        if txt.lower() in ("exit", "quit"):
            break
        if not txt.endswith("."):
            txt += "."
        try:
            tree = parser.parse(txt)
            print("Parse Tree:")
            print(tree.pretty())
            ast = ASTBuilder().transform(tree)
            print("AST:")
            print(ast)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()