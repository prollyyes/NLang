#!/usr/bin/env python3
"""
scripts/run_demo.py

Simple script to run the NLang demo.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Run the NLang demo."""
    print("NLang Demo - Natural Language Programming")
    print("=" * 50)
    
    # Check if dependencies are installed
    try:
        import lark
        print("✓ Lark parser library found")
    except ImportError:
        print("✗ Lark parser library not found")
        print("Please install dependencies with: pip install -r requirements.txt")
        return
    
    # Run the REPL
    try:
        from nlang_repl import NLangREPL
        repl = NLangREPL()
        repl.run()
    except Exception as e:
        print(f"Error starting REPL: {e}")
        print("Falling back to basic demo...")
        
        # Fallback to basic demo
        try:
            from parser.nlang_parser import NLangParser
            from parser.transpiler import NLangToPython
            
            parser = NLangParser()
            transpiler = NLangToPython()
            
            print("\nBasic Demo Mode:")
            print("Try these examples:")
            print("  let x be 5.")
            print("  print \"Hello world\".")
            print("  define y as 10.")
            
            while True:
                try:
                    text = input("\nnlang> ")
                    if text.lower() in ("exit", "quit"):
                        break
                    
                    # Process the input
                    python_code = transpiler.convert(text)
                    print(f"Generated Python: {python_code}")
                    
                except (EOFError, KeyboardInterrupt):
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    
        except Exception as e:
            print(f"Error in fallback mode: {e}")

if __name__ == "__main__":
    main() 