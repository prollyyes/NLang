#!/usr/bin/env python3
"""
scripts/simple_test.py

Very simple test to isolate the parsing issue.
"""

from lark import Lark

# Very simple grammar for testing
simple_grammar = """
start: statement "."

statement: let_statement
         | print_statement

let_statement: "let" IDENTIFIER "be" value
print_statement: "print" value

value: NUMBER
     | STRING
     | IDENTIFIER

IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+/
STRING: /"[^"]*"/

%import common.WS
%ignore WS
"""

def test_simple_grammar():
    """Test with a very simple grammar."""
    print("Testing simple grammar...")
    
    try:
        parser = Lark(simple_grammar, parser='lalr', start='start')
        print("✓ Simple grammar loaded")
        
        test_cases = [
            "let x be 5.",
            "print \"hello\".",
        ]
        
        for test in test_cases:
            try:
                tree = parser.parse(test)
                print(f"✓ Parsed: {test}")
                print(f"  Tree: {tree.pretty()}")
            except Exception as e:
                print(f"✗ Failed to parse: {test}")
                print(f"  Error: {e}")
                
    except Exception as e:
        print(f"✗ Simple grammar failed: {e}")

if __name__ == "__main__":
    test_simple_grammar() 