#!/usr/bin/env python3
"""
src/nlang_repl.py

Enhanced NLang REPL with execution capabilities.
"""

import sys
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from parser.nlang_parser import NLangParser, preprocess_natural_language
from parser.transpiler import NLangToPython

class NLangREPL:
    """Interactive REPL for NLang."""
    
    def __init__(self):
        self.parser = NLangParser()
        self.transpiler = NLangToPython()
        self.variables = {}
        self.history = []
        
    def run(self):
        """Start the REPL."""
        print("NLang REPL - Natural Language Programming")
        print("Type 'help' for commands, 'exit' to quit")
        print("=" * 50)
        
        while True:
            try:
                # Get input
                try:
                    text = input("nlang> ")
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break
                
                text = text.strip()
                if not text:
                    continue
                
                # Handle special commands
                if text.lower() in ("exit", "quit"):
                    print("Goodbye!")
                    break
                elif text.lower() == "help":
                    self._show_help()
                    continue
                elif text.lower() == "clear":
                    self.variables.clear()
                    print("Variables cleared.")
                    continue
                elif text.lower() == "vars":
                    self._show_variables()
                    continue
                elif text.lower().startswith("run "):
                    filename = text[4:].strip()
                    self._run_file(filename)
                    continue
                
                # Process NLang code
                self._process_input(text)
                
            except Exception as e:
                print(f"Error: {e}")
    
    def _process_input(self, text: str):
        """Process a single line of NLang input."""
        try:
            # Preprocess natural language
            processed = preprocess_natural_language(text)
            print(f"Processed: {processed}")
            
            # Parse to AST
            ast = self.parser.parse(processed)
            print(f"AST: {ast}")
            
            # Transpile to Python
            python_code = self.transpiler.convert(text)
            print(f"Python: {python_code}")
            
            # Execute the Python code
            result = self._execute_python(python_code)
            if result is not None:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Processing error: {e}")
    
    def _execute_python(self, python_code: str) -> Optional[Any]:
        """Execute Python code and return the result."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(python_code)
                temp_file = f.name
            
            # Execute the Python code
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            # Clean up
            os.unlink(temp_file)
            
            # Return output
            if result.stdout:
                return result.stdout.strip()
            elif result.stderr:
                return f"Error: {result.stderr.strip()}"
            else:
                return None
                
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out"
        except Exception as e:
            return f"Execution error: {e}"
    
    def _run_file(self, filename: str):
        """Run a NLang file."""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            print(f"Running {filename}...")
            print("=" * 30)
            
            # Process the file
            python_code = self.transpiler.convert(content)
            print("Generated Python:")
            print(python_code)
            print("=" * 30)
            
            # Execute
            result = self._execute_python(python_code)
            if result:
                print(f"Output: {result}")
                
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error running file: {e}")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
Available commands:
  help          - Show this help
  exit/quit     - Exit the REPL
  clear         - Clear all variables
  vars          - Show current variables
  run <file>    - Run a NLang file

NLang examples:
  let x be 5.
  define y as 10.
  print "Hello world".
  set z to x plus y.
  if x is 5, print "x equals 5".
        """
        print(help_text)
    
    def _show_variables(self):
        """Show current variables."""
        if self.variables:
            print("Current variables:")
            for name, value in self.variables.items():
                print(f"  {name} = {value}")
        else:
            print("No variables defined.")

def main():
    """Main entry point."""
    repl = NLangREPL()
    repl.run()

if __name__ == "__main__":
    main() 