"""
Semantic Analyzer for QuantumFlow Programming Language.
"""

from typing import Dict, Any, List, Optional
from parser import (
    ProgramNode, ModuleDefNode, AssignNode, WhenNode,
    CycleNode, YieldNode, ShowNode, BinaryOpNode,
    LiteralNode, VarNode, ASTNode
)

class Symbol:
    def __init__(self, name: str, sym_type: str, scope: str, line: int, value: Any = None):
        self.name = name
        self.type = sym_type
        self.scope = scope
        self.line = line
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "scope": self.scope,
            "line": self.line,
            "initial_value": str(self.value) if self.value is not None else "undefined"
        }

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table: List[Symbol] = []
        self.current_scope = "global"
        self.scopes: Dict[str, Dict[str, str]] = {"global": {}}
        self.errors: List[str] = []

    def log_error(self, message: str, line: int):
        self.errors.append(f"Semantic Error at line {line}: {message}")

    def analyze(self, ast: ProgramNode) -> Dict[str, Any]:
        self.symbol_table = []
        self.errors = []
        self.current_scope = "global"
        self.scopes = {"global": {}}

        for stmt in ast.statements:
            self.visit_statement(stmt)

        return {
            "success": len(self.errors) == 0,
            "errors": self.errors,
            "symbol_table": [s.to_dict() for s in self.symbol_table]
        }

    def is_declared(self, name: str) -> bool:
        if name in self.scopes.get(self.current_scope, {}):
            return True
        if name in self.scopes["global"]:
            return True
        return False

    def get_var_type(self, name: str) -> Optional[str]:
        if name in self.scopes.get(self.current_scope, {}):
            return self.scopes[self.current_scope][name]
        if name in self.scopes["global"]:
            return self.scopes["global"][name]
        return None

    def declare_var(self, name: str, var_type: str, line: int, val: Any = None):
        if self.current_scope not in self.scopes:
            self.scopes[self.current_scope] = {}
        self.scopes[self.current_scope][name] = var_type
        
        existing = next((s for s in self.symbol_table if s.name == name and s.scope == self.current_scope), None)
        if not existing:
            self.symbol_table.append(Symbol(name, var_type, self.current_scope, line, val))
        else:
            existing.type = var_type
            if val is not None:
                existing.value = val

    def visit_statement(self, node: ASTNode):
        if isinstance(node, ProgramNode):
            for s in node.statements:
                self.visit_statement(s)

        elif isinstance(node, ModuleDefNode):
            self.declare_var(node.name, "module", node.line, f"params({','.join(node.params)})")
            
            prev_scope = self.current_scope
            self.current_scope = f"module_{node.name}"
            self.scopes[self.current_scope] = {}
            
            for p in node.params:
                self.declare_var(p, "parameter", node.line)

            for stmt in node.body:
                self.visit_statement(stmt)
                
            self.current_scope = prev_scope

        elif isinstance(node, AssignNode):
            val_type = self.infer_type(node.value)
            val = node.value.value if isinstance(node.value, LiteralNode) else None
            self.declare_var(node.name, val_type or "dynamic", node.line, val)

        elif isinstance(node, WhenNode):
            self.infer_type(node.condition)
            for stmt in node.then_branch:
                self.visit_statement(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self.visit_statement(stmt)

        elif isinstance(node, CycleNode):
            self.infer_type(node.condition)
            for stmt in node.body:
                self.visit_statement(stmt)

        elif isinstance(node, YieldNode):
            self.infer_type(node.value)

        elif isinstance(node, ShowNode):
            self.infer_type(node.expr)

    def infer_type(self, node: ASTNode) -> str:
        if isinstance(node, LiteralNode):
            return node.lit_type

        elif isinstance(node, VarNode):
            if not self.is_declared(node.name):
                self.log_error(f"Variable '{node.name}' used before declaration/assignment.", node.line)
                return "unknown"
            return self.get_var_type(node.name) or "unknown"

        elif isinstance(node, BinaryOpNode):
            left_t = self.infer_type(node.left)
            right_t = self.infer_type(node.right)
            
            if node.op in ('==?', '!=?', '>>>', '<<<', '&&&', '|||'):
                return "BOOLEAN"
            
            if node.op in ('.+.', '.-.', '.*.', './.'):
                if left_t == "STRING" or right_t == "STRING":
                    if node.op == '.+.':
                        return "STRING"
                    else:
                        self.log_error(f"Cannot perform '{node.op}' on STRING values.", node.line)
                        return "unknown"
                return "NUMBER"

        return "dynamic"
