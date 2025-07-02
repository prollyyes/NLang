#!/usr/bin/env python3
"""
src/parser/nlang_parser.py

Enhanced NLang parser with natural language constructs and AST generation.
"""

from lark import Lark, Transformer, v_args
from typing import Dict, List, Any, Optional
import re

class NLangASTBuilder(Transformer):
    """Transform parse trees into structured AST nodes."""
    
    def __default__(self, data, children, meta):
        return {"type": data, "children": children}
    
    # Statement types
    def let_statement(self, children):      return {"type": "let", "children": children}
    def define_statement(self, children):   return {"type": "define", "children": children}
    def print_statement(self, children):    return {"type": "print", "children": children}
    def import_statement(self, children):   return {"type": "import", "children": children}
    
    # Expression types
    def IDENTIFIER(self, token):           return {"type": "identifier", "value": str(token)}
    def NUMBER(self, token):               return {"type": "number", "value": float(token)}
    def STRING(self, token):               return {"type": "string", "value": token[1:-1]}
    
    # Values and expressions
    def value(self, children):             return {"type": "value", "children": children}

class NLangParser:
    """Main parser for NLang programs."""
    
    def __init__(self):
        self.parser = Lark.open('grammar/nlang_working.lark', parser='lalr', start='start')
        self.transformer = NLangASTBuilder()
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse NLang text into an AST."""
        # Ensure text ends with period if not already
        if not text.strip().endswith('.'):
            text = text.strip() + '.'
        
        try:
            tree = self.parser.parse(text)
            ast = self.transformer.transform(tree)
            return ast
        except Exception as e:
            raise ParseError(f"Failed to parse: {e}")
    
    def parse_program(self, text: str) -> List[Dict[str, Any]]:
        """Parse a multi-line NLang program."""
        statements = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    ast = self.parse(line)
                    statements.append(ast)
                except ParseError as e:
                    print(f"Warning: Could not parse line '{line}': {e}")
        
        return statements

class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass

# Natural language preprocessing
def preprocess_natural_language(text: str) -> str:
    """Convert natural language constructs to formal syntax."""
    # Convert common natural language patterns
    patterns = [
        (r'\bcreate\b', 'define'),
        (r'\bmake\b', 'define'),
        (r'\bassign\b', 'set'),
        (r'\bput\b', 'set'),
        (r'\bshow\b', 'print'),
        (r'\bdisplay\b', 'print'),
        (r'\bsay\b', 'print'),
        (r'\bannounce\b', 'print'),
        (r'\bmultiplied by\b', '*'),
        (r'\bdivided by\b', '/'),
        (r'\bplus\b', '+'),
        (r'\bminus\b', '-'),
        (r'\btimes\b', '*'),
        (r'\bexceeds\b', '>'),
        (r'\bis at least\b', '>='),
        (r'\bis less than\b', '<'),
        (r'\bequals\b', '=='),
        (r'\bis\b', '=='),
    ]
    
    processed = text.lower()
    for pattern, replacement in patterns:
        processed = re.sub(pattern, replacement, processed)
    
    return processed 