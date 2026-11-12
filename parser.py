"""
Syntax Analyzer (Parser) for QuantumFlow Programming Language.
Supports both block delimited by 'initiate' ... 'end' AND single-statement blocks.
"""

from typing import List, Any, Dict, Optional
from lexer import Token

class ASTNode:
    """Base class for all AST nodes."""
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "Program",
            "body": [stmt.to_dict() for stmt in self.statements]
        }

class ModuleDefNode(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode], line: int):
        self.name = name
        self.params = params
        self.body = body
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": f"Module: {self.name}({', '.join(self.params)})",
            "body": [s.to_dict() for s in self.body],
            "line": self.line
        }

class AssignNode(ASTNode):
    def __init__(self, name: str, value: ASTNode, line: int):
        self.name = name
        self.value = value
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": f"Assign: {self.name} :=",
            "value": self.value.to_dict(),
            "line": self.line
        }

class WhenNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: Optional[List[ASTNode]], line: int):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "node": "When (Condition)",
            "condition": self.condition.to_dict(),
            "then": [s.to_dict() for s in self.then_branch],
            "line": self.line
        }
        if self.else_branch:
            res["otherwise"] = [s.to_dict() for s in self.else_branch]
        return res

class CycleNode(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int):
        self.condition = condition
        self.body = body
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "Cycle (Loop)",
            "condition": self.condition.to_dict(),
            "body": [s.to_dict() for s in self.body],
            "line": self.line
        }

class YieldNode(ASTNode):
    def __init__(self, value: ASTNode, line: int):
        self.value = value
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "Yield",
            "value": self.value.to_dict(),
            "line": self.line
        }

class ShowNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int):
        self.expr = expr
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "Show()",
            "argument": self.expr.to_dict(),
            "line": self.line
        }

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int):
        self.left = left
        self.op = op
        self.right = right
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": f"Op: {self.op}",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "line": self.line
        }

class LiteralNode(ASTNode):
    def __init__(self, value: Any, lit_type: str, line: int):
        self.value = value
        self.lit_type = lit_type
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": f"{self.lit_type}: {repr(self.value)}",
            "line": self.line
        }

class VarNode(ASTNode):
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": f"Var: {self.name}",
            "line": self.line
        }


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def match(self, expected_type: str) -> Token:
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(
            f"Syntax Error at line {token.line}, col {token.column}: "
            f"Expected '{expected_type}', found '{token.value or token.type}'"
        )

    def parse(self) -> ProgramNode:
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.statement())
        return ProgramNode(statements)

    def statement(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == 'KW_MODULE':
            return self.module_definition()
        elif token.type == 'KW_INITIATE':
            stmts = self.block_or_statements()
            return stmts[0] if len(stmts) == 1 else ProgramNode(stmts)
        elif token.type == 'KW_WHEN':
            return self.when_statement()
        elif token.type == 'KW_CYCLE':
            return self.cycle_statement()
        elif token.type == 'KW_YIELD':
            return self.yield_statement()
        elif token.type == 'KW_SHOW':
            return self.show_statement()
        elif token.type == 'IDENTIFIER':
            return self.assignment_statement()
        else:
            raise SyntaxError(
                f"Syntax Error at line {token.line}: Unexpected statement starting with '{token.value}'"
            )

    def module_definition(self) -> ModuleDefNode:
        kw = self.match('KW_MODULE')
        name_tok = self.match('IDENTIFIER')
        self.match('LPAREN')
        params = []
        if self.current_token().type == 'IDENTIFIER':
            params.append(self.match('IDENTIFIER').value)
            while self.current_token().type == 'COMMA':
                self.match('COMMA')
                params.append(self.match('IDENTIFIER').value)
        self.match('RPAREN')
        self.match('COLON')
        body = self.block_or_statements()
        return ModuleDefNode(name_tok.value, params, body, kw.line)

    def block_or_statements(self) -> List[ASTNode]:
        """
        Parses either:
        1. An explicit block: 'initiate' ... optional 'end' or until next branch delimiter
        2. Or a single statement
        """
        statements = []
        if self.current_token().type == 'KW_INITIATE':
            self.match('KW_INITIATE')
            while self.current_token().type not in ('KW_END', 'KW_OTHERWISE', 'EOF'):
                statements.append(self.statement())
            if self.current_token().type == 'KW_END':
                self.match('KW_END')
        else:
            statements.append(self.statement())
        return statements

    def assignment_statement(self) -> AssignNode:
        id_tok = self.match('IDENTIFIER')
        self.match('OP_ASSIGN')
        val_node = self.expr()
        return AssignNode(id_tok.value, val_node, id_tok.line)

    def when_statement(self) -> WhenNode:
        kw = self.match('KW_WHEN')
        condition = self.expr()
        then_branch = self.block_or_statements()
        else_branch = None
        if self.current_token().type == 'KW_OTHERWISE':
            self.match('KW_OTHERWISE')
            else_branch = self.block_or_statements()
        return WhenNode(condition, then_branch, else_branch, kw.line)

    def cycle_statement(self) -> CycleNode:
        kw = self.match('KW_CYCLE')
        condition = self.expr()
        body = self.block_or_statements()
        return CycleNode(condition, body, kw.line)

    def yield_statement(self) -> YieldNode:
        kw = self.match('KW_YIELD')
        val = self.expr()
        return YieldNode(val, kw.line)

    def show_statement(self) -> ShowNode:
        kw = self.match('KW_SHOW')
        self.match('LPAREN')
        expr = self.expr()
        self.match('RPAREN')
        return ShowNode(expr, kw.line)

    def expr(self) -> ASTNode:
        return self.logical_or()

    def logical_or(self) -> ASTNode:
        node = self.logical_and()
        while self.current_token().type == 'OP_OR':
            op_tok = self.match('OP_OR')
            right = self.logical_and()
            node = BinaryOpNode(node, op_tok.value, right, op_tok.line)
        return node

    def logical_and(self) -> ASTNode:
        node = self.relational()
        while self.current_token().type == 'OP_AND':
            op_tok = self.match('OP_AND')
            right = self.relational()
            node = BinaryOpNode(node, op_tok.value, right, op_tok.line)
        return node

    def relational(self) -> ASTNode:
        node = self.additive()
        if self.current_token().type in ('OP_EQ', 'OP_NEQ', 'OP_GT', 'OP_LT'):
            op_tok = self.match(self.current_token().type)
            right = self.additive()
            node = BinaryOpNode(node, op_tok.value, right, op_tok.line)
        return node

    def additive(self) -> ASTNode:
        node = self.multiplicative()
        while self.current_token().type in ('OP_ADD', 'OP_SUB'):
            op_tok = self.match(self.current_token().type)
            right = self.multiplicative()
            node = BinaryOpNode(node, op_tok.value, right, op_tok.line)
        return node

    def multiplicative(self) -> ASTNode:
        node = self.primary()
        while self.current_token().type in ('OP_MUL', 'OP_DIV'):
            op_tok = self.match(self.current_token().type)
            right = self.primary()
            node = BinaryOpNode(node, op_tok.value, right, op_tok.line)
        return node

    def primary(self) -> ASTNode:
        tok = self.current_token()
        if tok.type == 'NUMBER':
            self.match('NUMBER')
            val = float(tok.value) if '.' in tok.value else int(tok.value)
            return LiteralNode(val, 'NUMBER', tok.line)
        elif tok.type == 'STRING':
            self.match('STRING')
            return LiteralNode(tok.value[1:-1], 'STRING', tok.line)
        elif tok.type == 'IDENTIFIER':
            self.match('IDENTIFIER')
            return VarNode(tok.value, tok.line)
        elif tok.type == 'LPAREN':
            self.match('LPAREN')
            sub_expr = self.expr()
            self.match('RPAREN')
            return sub_expr
        else:
            raise SyntaxError(
                f"Syntax Error at line {tok.line}: Unexpected token '{tok.value}' in expression."
            )

def parse_code(tokens: List[Token]) -> ProgramNode:
    parser = Parser(tokens)
    return parser.parse()
