# Lab 3 - Semantic Analysis: symbol table + type checking on the Lab 2 tree
import sys
from lab2_parser import parse_file

TYPE_OF_KEYWORD = {"INT": "int", "BOOL": "pulse", "STRING": "wave"}

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}      # name -> {"type": ..., "line": ...}
        self.errors = []

    def error(self, line, msg):
        self.errors.append(f"Semantic Error at line {line}: {msg}")

    def visit(self, stmts):
        for s in stmts:
            tag = s[0]
            if tag == "decl":
                _, typ, name, init, line = s
                if name in self.symbols:
                    self.error(line, f"variable '{name}' is already declared at line {self.symbols[name]['line']}")
                else:
                    self.symbols[name] = {"type": typ, "line": line}
                if init is not None:
                    got = self.type_of(init)
                    if got and got != typ:
                        self.error(line, f"cannot store {got} value in {typ} variable '{name}'")
            elif tag == "assign":
                _, name, value, line = s
                got = self.type_of(value)
                if name not in self.symbols:
                    self.error(line, f"variable '{name}' is not declared")
                elif got and got != self.symbols[name]["type"]:
                    self.error(line, f"cannot store {got} value in {self.symbols[name]['type']} variable '{name}'")
            elif tag in ("if", "while"):
                got = self.type_of(s[1])
                if got and got != "pulse":
                    self.error(s[-1], f"condition must be pulse but it is {got}")
                self.visit(s[2])
                if tag == "if" and s[3] is not None:
                    self.visit(s[3])
            elif tag == "print":
                self.type_of(s[1])

    def type_of(self, e):
        """Returns 'int', 'pulse', 'wave', or None when the type is unknown because of an error."""
        tag = e[0]
        if tag == "num":
            return "int"
        if tag == "str":
            return "wave"
        if tag == "bool":
            return "pulse"
        if tag == "id":
            if e[1] not in self.symbols:
                self.error(e[2], f"variable '{e[1]}' is not declared")
                return None
            return self.symbols[e[1]]["type"]
        _, op, left, right, line = e
        lt, rt = self.type_of(left), self.type_of(right)
        if lt is None or rt is None:
            return None
        if op in (".+.", ".-.", ".*.", "./."):
            if lt != "int" or rt != "int":
                self.error(line, f"operator '{op}' needs int operands but got {lt} and {rt}")
                return None
            return "int"
        if op in ("<<<", ">>>"):
            if lt != "int" or rt != "int":
                self.error(line, f"operator '{op}' needs int operands but got {lt} and {rt}")
                return None
            return "pulse"
        if lt != rt:                                   # ==? and !=?
            self.error(line, f"operator '{op}' cannot compare {lt} with {rt}")
            return None
        return "pulse"

def analyze(tree):
    sa = SemanticAnalyzer()
    sa.visit(tree)
    return sa

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab3_semantic.py <filename>")
        sys.exit(1)
    try:
        tree = parse_file(sys.argv[1])
    except SyntaxError as e:
        sys.exit(str(e))
    sa = analyze(tree)
    print("Symbol Table")
    print("------------")
    print(f"{'Name':<10}{'Type':<10}{'Declared at line'}")
    for name, info in sa.symbols.items():
        print(f"{name:<10}{info['type']:<10}{info['line']}")
    print()
    for err in sa.errors:
        print(err)
    if sa.errors:
        print(f"\nRESULT: {len(sa.errors)} semantic error(s) found")
    else:
        print("RESULT: No semantic errors")

