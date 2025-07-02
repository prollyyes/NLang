#!/usr/bin/env python3
"""
src/parser/transpiler.py

Transpiler that converts NLang AST to Python code.
"""

from typing import Dict, List, Any, Optional
import ast as python_ast

class NLangTranspiler:
    """Convert NLang AST to Python code."""
    
    def __init__(self):
        self.indent_level = 0
        self.variables = set()
        self.imports = set()
    
    def transpile(self, ast: Dict[str, Any]) -> str:
        """Convert a single AST node to Python code."""
        node_type = ast.get("type")
        
        if node_type == "let":
            return self._transpile_let(ast)
        elif node_type == "define":
            return self._transpile_define(ast)
        elif node_type == "set":
            return self._transpile_set(ast)
        elif node_type == "print":
            return self._transpile_print(ast)
        elif node_type == "if":
            return self._transpile_if(ast)
        elif node_type == "for":
            return self._transpile_for(ast)
        elif node_type == "while":
            return self._transpile_while(ast)
        elif node_type == "import":
            return self._transpile_import(ast)
        elif node_type == "return":
            return self._transpile_return(ast)
        else:
            return self._transpile_expression(ast)
    
    def transpile_program(self, statements: List[Dict[str, Any]]) -> str:
        """Convert a list of AST statements to a complete Python program."""
        lines = []
        
        # Add standard imports
        lines.append("#!/usr/bin/env python3")
        lines.append('"""Generated Python code from NLang."""')
        lines.append("")
        
        # Add any required imports
        if self.imports:
            for imp in sorted(self.imports):
                lines.append(f"import {imp}")
            lines.append("")
        
        # Transpile each statement
        for statement in statements:
            # Extract the actual statement from the AST
            if statement.get("type") == "start":
                # Get the statement from the start node
                statement_node = statement.get("children", [{}])[0]
                if statement_node.get("type") == "statement":
                    actual_statement = statement_node.get("children", [{}])[0]
                    python_code = self.transpile(actual_statement)
                    if python_code:
                        lines.append(python_code)
            else:
                python_code = self.transpile(statement)
                if python_code:
                    lines.append(python_code)
        
        return "\n".join(lines)
    
    def _transpile_let(self, ast: Dict[str, Any]) -> str:
        """Transpile 'let' statements (variable declarations)."""
        children = ast.get("children", [])
        if len(children) >= 2:
            var_name = self._extract_identifier(children[0])
            value = self._transpile_expression(children[1])
            self.variables.add(var_name)
            return f"{var_name} = {value}"
        return ""
    
    def _transpile_define(self, ast: Dict[str, Any]) -> str:
        """Transpile 'define' statements (variable assignments)."""
        children = ast.get("children", [])
        if len(children) >= 2:
            var_name = self._extract_identifier(children[0])
            value = self._transpile_expression(children[1])
            self.variables.add(var_name)
            return f"{var_name} = {value}"
        return ""
    
    def _transpile_set(self, ast: Dict[str, Any]) -> str:
        """Transpile 'set' statements (variable assignments)."""
        return self._transpile_define(ast)
    
    def _transpile_print(self, ast: Dict[str, Any]) -> str:
        """Transpile 'print' statements."""
        children = ast.get("children", [])
        if children:
            value = self._transpile_expression(children[0])
            return f"print({value})"
        return "print()"
    
    def _transpile_if(self, ast: Dict[str, Any]) -> str:
        """Transpile 'if' statements."""
        children = ast.get("children", [])
        if len(children) >= 2:
            condition = self._transpile_expression(children[0])
            body = self._transpile_expression(children[1])
            return f"if {condition}:\n    {body}"
        return ""
    
    def _transpile_for(self, ast: Dict[str, Any]) -> str:
        """Transpile 'for' statements."""
        children = ast.get("children", [])
        if len(children) >= 2:
            iterator = self._extract_identifier(children[0])
            collection = self._transpile_expression(children[1])
            return f"for {iterator} in {collection}:"
        return ""
    
    def _transpile_while(self, ast: Dict[str, Any]) -> str:
        """Transpile 'while' statements."""
        children = ast.get("children", [])
        if len(children) >= 1:
            condition = self._transpile_expression(children[0])
            return f"while {condition}:"
        return ""
    
    def _transpile_import(self, ast: Dict[str, Any]) -> str:
        """Transpile 'import' statements."""
        children = ast.get("children", [])
        if children:
            module = self._extract_identifier(children[0])
            self.imports.add(module)
            return f"import {module}"
        return ""
    
    def _transpile_return(self, ast: Dict[str, Any]) -> str:
        """Transpile 'return' statements."""
        children = ast.get("children", [])
        if children:
            value = self._transpile_expression(children[0])
            return f"return {value}"
        return "return"
    
    def _transpile_expression(self, ast: Dict[str, Any]) -> str:
        """Transpile expressions."""
        if not isinstance(ast, dict):
            return str(ast)
        
        node_type = ast.get("type")
        
        if node_type == "identifier":
            return ast.get("value", "")
        elif node_type == "number":
            return str(ast.get("value", 0))
        elif node_type == "string":
            return f'"{ast.get("value", "")}"'
        elif node_type == "boolean":
            return str(ast.get("value", False))
        elif node_type == "value":
            # Handle value nodes (which contain the actual value)
            children = ast.get("children", [])
            if len(children) == 1:
                return self._transpile_expression(children[0])
            elif len(children) == 2:
                # Handle binary operations like "5 plus 3"
                left = self._transpile_expression(children[0])
                right = self._transpile_expression(children[1])
                return f"{left} + {right}"  # Default to addition for now
            else:
                return str(children)
        elif node_type == "in_clause":
            return self._transpile_in_clause(ast)
        elif node_type == "where_clause":
            return self._transpile_where_clause(ast)
        else:
            # Handle complex expressions
            children = ast.get("children", [])
            if len(children) == 1:
                return self._transpile_expression(children[0])
            elif len(children) == 2:
                left = self._transpile_expression(children[0])
                right = self._transpile_expression(children[1])
                return f"{left} {right}"
            else:
                return str(children)
    
    def _transpile_in_clause(self, ast: Dict[str, Any]) -> str:
        """Transpile 'in' clauses."""
        children = ast.get("children", [])
        if children:
            return self._transpile_expression(children[0])
        return ""
    
    def _transpile_where_clause(self, ast: Dict[str, Any]) -> str:
        """Transpile 'where' clauses."""
        children = ast.get("children", [])
        if children:
            return self._transpile_expression(children[0])
        return ""
    
    def _extract_identifier(self, ast: Dict[str, Any]) -> str:
        """Extract identifier value from AST node."""
        if isinstance(ast, dict) and ast.get("type") == "identifier":
            return ast.get("value", "")
        elif isinstance(ast, str):
            return ast
        else:
            return str(ast)

class NLangToPython:
    """High-level interface for converting NLang to Python."""
    
    def __init__(self):
        self.transpiler = NLangTranspiler()
    
    def convert(self, nlang_code: str) -> str:
        """Convert NLang code to Python."""
        from .nlang_parser import NLangParser, preprocess_natural_language
        
        # Preprocess natural language
        processed_code = preprocess_natural_language(nlang_code)
        
        # Parse into AST
        parser = NLangParser()
        statements = parser.parse_program(processed_code)
        
        # Transpile to Python
        python_code = self.transpiler.transpile_program(statements)
        
        return python_code 