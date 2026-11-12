"""
Virtual Machine / Evaluator for QuantumFlow.
"""

from typing import Dict, Any, List
from parser import (
    ProgramNode, ModuleDefNode, AssignNode, WhenNode,
    CycleNode, YieldNode, ShowNode, BinaryOpNode,
    LiteralNode, VarNode, ASTNode
)

class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value

class Evaluator:
    def __init__(self, max_cycles: int = 1000):
        self.env: Dict[str, Any] = {}
        self.modules: Dict[str, ModuleDefNode] = {}
        self.stdout: List[str] = []
        self.max_cycles = max_cycles
        self.cycle_count = 0

    def run(self, ast: ProgramNode) -> Dict[str, Any]:
        self.env = {}
        self.modules = {}
        self.stdout = []
        self.cycle_count = 0
        final_yield = None

        try:
            for stmt in ast.statements:
                self.eval_stmt(stmt)
        except ReturnSignal as ret:
            final_yield = ret.value
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "\n".join(self.stdout),
                "variables": self.env
            }

        return {
            "success": True,
            "output": "\n".join(self.stdout),
            "yield_value": final_yield,
            "variables": self.env
        }

    def eval_stmt(self, node: ASTNode):
        if isinstance(node, ProgramNode):
            for s in node.statements:
                self.eval_stmt(s)

        elif isinstance(node, ModuleDefNode):
            self.modules[node.name] = node
            for stmt in node.body:
                self.eval_stmt(stmt)

        elif isinstance(node, AssignNode):
            val = self.eval_expr(node.value)
            self.env[node.name] = val

        elif isinstance(node, WhenNode):
            cond = self.eval_expr(node.condition)
            if cond:
                for stmt in node.then_branch:
                    self.eval_stmt(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self.eval_stmt(stmt)

        elif isinstance(node, CycleNode):
            while self.eval_expr(node.condition):
                self.cycle_count += 1
                if self.cycle_count > self.max_cycles:
                    raise RuntimeError("Infinite loop protection: cycle limit exceeded.")
                for stmt in node.body:
                    self.eval_stmt(stmt)

        elif isinstance(node, YieldNode):
            val = self.eval_expr(node.value)
            raise ReturnSignal(val)

        elif isinstance(node, ShowNode):
            val = self.eval_expr(node.expr)
            self.stdout.append(str(val))

    def eval_expr(self, node: ASTNode) -> Any:
        if isinstance(node, LiteralNode):
            return node.value

        elif isinstance(node, VarNode):
            if node.name not in self.env:
                raise NameError(f"Runtime Error: Variable '{node.name}' not found.")
            return self.env[node.name]

        elif isinstance(node, BinaryOpNode):
            left = self.eval_expr(node.left)
            right = self.eval_expr(node.right)

            if node.op == '.+.':
                return left + right
            elif node.op == '.-.':
                return left - right
            elif node.op == '.*.':
                return left * right
            elif node.op == './.':
                if right == 0:
                    raise ZeroDivisionError("Runtime Error: Division by zero.")
                return left / right
            elif node.op == '==?':
                return left == right
            elif node.op == '!=?':
                return left != right
            elif node.op == '>>>':
                return left > right
            elif node.op == '<<<':
                return left < right
            elif node.op == '&&&':
                return bool(left and right)
            elif node.op == '|||':
                return bool(left or right)
            else:
                raise ValueError(f"Unknown operator: {node.op}")

        return None
