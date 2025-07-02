#!/usr/bin/env python3
"""
scripts/test_working_grammar.py

Test the working grammar.
"""

from lark import Lark

def test_working_grammar():
    """Test the working grammar."""
    print("Testing working grammar...")
    
    try:
        parser = Lark.open('grammar/nlang_working.lark', parser='lalr', start='start')
        print("✓ Working grammar loaded")
        
        test_cases = [
            "let x be 5.",
            "let x be 5 plus 3.",
            "define y as 10.",
            "define y as 2 times 3.",
            "print \"Hello world\".",
            "import pandas.",
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
        print(f"✗ Working grammar failed: {e}")

if __name__ == "__main__":
    test_working_grammar() 