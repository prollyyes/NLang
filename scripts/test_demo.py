#!/usr/bin/env python3
"""
scripts/test_demo.py

Test script to verify NLang implementation.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parser.nlang_parser import NLangParser, preprocess_natural_language
from parser.transpiler import NLangToPython

def test_basic_parsing():
    """Test basic parsing functionality."""
    print("Testing basic parsing...")
    
    parser = NLangParser()
    test_cases = [
        "let x be 5.",
        "define y as 10.",
        "print \"Hello world\".",
        "set z to x plus y.",
    ]
    
    for test in test_cases:
        try:
            ast = parser.parse(test)
            print(f"✓ Parsed: {test}")
            print(f"  AST: {ast}")
        except Exception as e:
            print(f"✗ Failed to parse: {test}")
            print(f"  Error: {e}")
    
    print()

def test_natural_language():
    """Test natural language preprocessing."""
    print("Testing natural language preprocessing...")
    
    test_cases = [
        ("create x as 5", "define x as 5"),
        ("make y be 10", "define y be 10"),
        ("show \"Hello\"", "print \"Hello\""),
        ("x multiplied by y", "x * y"),
        ("a plus b", "a + b"),
    ]
    
    for input_text, expected in test_cases:
        processed = preprocess_natural_language(input_text)
        print(f"Input: {input_text}")
        print(f"Processed: {processed}")
        print(f"Expected: {expected}")
        print()

def test_transpilation():
    """Test transpilation to Python."""
    print("Testing transpilation...")
    
    transpiler = NLangToPython()
    test_cases = [
        ("let x be 5.", "x = 5"),
        ("print \"Hello\".", "print(\"Hello\")"),
        ("define y as 10.", "y = 10"),
    ]
    
    for nlang_code, expected_python in test_cases:
        try:
            python_code = transpiler.convert(nlang_code)
            print(f"NLang: {nlang_code}")
            print(f"Python: {python_code}")
            print()
        except Exception as e:
            print(f"✗ Failed to transpile: {nlang_code}")
            print(f"  Error: {e}")
    
    print()

def test_example_files():
    """Test parsing example files."""
    print("Testing example files...")
    
    example_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    transpiler = NLangToPython()
    
    for filename in os.listdir(example_dir):
        if filename.endswith('.nlang'):
            filepath = os.path.join(example_dir, filename)
            print(f"Testing {filename}...")
            
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                
                python_code = transpiler.convert(content)
                print(f"Generated Python code:")
                print(python_code)
                print("-" * 40)
                
            except Exception as e:
                print(f"✗ Failed to process {filename}: {e}")
    
    print()

def main():
    """Run all tests."""
    print("NLang Demo Test Suite")
    print("=" * 50)
    
    test_basic_parsing()
    test_natural_language()
    test_transpilation()
    test_example_files()
    
    print("Test suite completed!")

if __name__ == "__main__":
    main() 