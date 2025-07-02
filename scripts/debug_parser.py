#!/usr/bin/env python3
"""
scripts/debug_parser.py

Debug script to test the NLang parser step by step.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_grammar():
    """Test if the grammar loads correctly."""
    print("Testing grammar loading...")
    try:
        from lark import Lark
        parser = Lark.open('grammar/nlang_working.lark', parser='lalr', start='start')
        print("✓ Grammar loaded successfully")
        return parser
    except Exception as e:
        print(f"✗ Grammar loading failed: {e}")
        return None

def test_basic_parsing(parser):
    """Test basic parsing with simple and compound expressions."""
    print("\nTesting basic parsing...")
    
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

def test_ast_building():
    """Test AST building."""
    print("\nTesting AST building...")
    try:
        from parser.nlang_parser import NLangParser
        parser = NLangParser()
        print("✓ AST parser created")
        
        # Test simple and compound cases
        test_cases = [
            "let x be 5.",
            "let x be 5 plus 3.",
            "print \"Hello\".",
        ]
        
        for test in test_cases:
            try:
                ast = parser.parse(test)
                print(f"✓ AST for '{test}': {ast}")
            except Exception as e:
                print(f"✗ AST failed for '{test}': {e}")
                
    except Exception as e:
        print(f"✗ AST building failed: {e}")

def main():
    """Run all debug tests."""
    print("NLang Parser Debug")
    print("=" * 30)
    
    # Test grammar
    parser = test_grammar()
    if parser:
        test_basic_parsing(parser)
    
    # Test AST building
    test_ast_building()

if __name__ == "__main__":
    main() 