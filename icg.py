"""
Intermediate Code Generator (ICG) for QuantumFlow Programming Language.
Produces Three-Address Code (3AC) instructions.
"""

from typing import List, Tuple, Dict, Any
from parser import (
    ProgramNode, ModuleDefNode, AssignNode, WhenNode,
    CycleNode, YieldNode, ShowNode, BinaryOpNode,
    LiteralNode, VarNode, ASTNode
)

class Instruction:
    def __init__(self, op: str, arg1: str = "", arg2: str = "", result: str = ""):
        self.op = op
        self.arg1 = str(arg1)
        self.arg2 = str(arg2)
        self.result = str(result)

    def __str__(self) -> str:
        if self.op == 'LABEL':
            return f"{self.result}:"
        elif self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'GOTO':
            return f"goto {self.result}"
        elif self.op == 'IF_FALSE':
            return f"if_false {self.arg1} goto {self.result}"
        elif self.op == 'SHOW':
            return f"param {self.arg1}\ncall show, 1"
        elif self.op == 'YIELD':
            return f"yield {self.arg1}"
        elif self.op == 'FUNC_START':
            return f"func_start {self.arg1}"
        elif self.op == 'FUNC_END':
            return f"func_end {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

    def to_dict(self) -> Dict[str, str]:
        return {
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "result": self.result,
            "text": str(self)
        }


class CodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions: List[Instruction] = []

    def new_temp(self) -> str:
        t = f"t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def new_label(self) -> str:
        l = f"L{self.label_counter}"
        self.label_counter += 1
        return l

    def emit(self, op: str, arg1: str = "", arg2: str = "", result: str = "") -> Instruction:
        instr = Instruction(op, arg1, arg2, result)
        self.instructions.append(instr)
        return instr

    def generate(self, ast: ProgramNode) -> List[Instruction]:
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions = []
        for stmt in ast.statements:
            self.gen_stmt(stmt)
        return self.instructions

    def gen_stmt(self, node: ASTNode):
        if isinstance(node, ProgramNode):
            for s in node.statements:
                self.gen_stmt(s)

        elif isinstance(node, ModuleDefNode):
            self.emit('FUNC_START', node.name)
            for stmt in node.body:
                self.gen_stmt(stmt)
            self.emit('FUNC_END', node.name)

        elif isinstance(node, AssignNode):
            val_place = self.gen_expr(node.value)
            self.emit('ASSIGN', val_place, result=node.name)

        elif isinstance(node, WhenNode):
            cond_place = self.gen_expr(node.condition)
            label_else = self.new_label()
            label_end = self.new_label()

            self.emit('IF_FALSE', cond_place, result=label_else)
            for stmt in node.then_branch:
                self.gen_stmt(stmt)

            if node.else_branch:
                self.emit('GOTO', result=label_end)
                self.emit('LABEL', result=label_else)
                for stmt in node.else_branch:
                    self.gen_stmt(stmt)
                self.emit('LABEL', result=label_end)
            else:
                self.emit('LABEL', result=label_else)

        elif isinstance(node, CycleNode):
            label_start = self.new_label()
            label_end = self.new_label()

            self.emit('LABEL', result=label_start)
            cond_place = self.gen_expr(node.condition)
            self.emit('IF_FALSE', cond_place, result=label_end)

            for stmt in node.body:
                self.gen_stmt(stmt)

            self.emit('GOTO', result=label_start)
            self.emit('LABEL', result=label_end)

        elif isinstance(node, YieldNode):
            val_place = self.gen_expr(node.value)
            self.emit('YIELD', val_place)

        elif isinstance(node, ShowNode):
            val_place = self.gen_expr(node.expr)
            self.emit('SHOW', val_place)

    def gen_expr(self, node: ASTNode) -> str:
        if isinstance(node, LiteralNode):
            if node.lit_type == 'STRING':
                return f'"{node.value}"'
            return str(node.value)

        elif isinstance(node, VarNode):
            return node.name

        elif isinstance(node, BinaryOpNode):
            left_p = self.gen_expr(node.left)
            right_p = self.gen_expr(node.right)
            temp = self.new_temp()
            self.emit(node.op, left_p, right_p, result=temp)
            return temp

        return ""
