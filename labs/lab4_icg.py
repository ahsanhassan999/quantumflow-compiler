# Lab 4 - Intermediate Code Generation: three-address code + quadruples
import sys
from lab2_parser import parse_file
from lab3_semantic import analyze

class CodeGenerator:
    def __init__(self):
        self.quads = []        # (op, arg1, arg2, result)
        self.temps = 0
        self.labels = 0

    def new_temp(self):
        self.temps += 1
        return f"t{self.temps}"

    def new_label(self):
        self.labels += 1
        return f"L{self.labels}"

    def emit(self, op, a1="", a2="", res=""):
        self.quads.append((op, a1, a2, res))

    def gen_expr(self, e):
        """Emits code for an expression and returns the name that holds its value."""
        tag = e[0]
        if tag == "bool":
            return "true" if e[1] == "true" else "false"
        if tag in ("num", "str", "id"):
            return e[1]
        _, op, left, right, _ = e
        a, b = self.gen_expr(left), self.gen_expr(right)
        t = self.new_temp()
        self.emit(op, a, b, t)
        return t

    def gen(self, stmts):
        for s in stmts:
            tag = s[0]
            if tag == "decl" and s[3] is not None:
                self.emit("=", self.gen_expr(s[3]), "", s[2])
            elif tag == "assign":
                self.emit("=", self.gen_expr(s[2]), "", s[1])
            elif tag == "print":
                self.emit("print", self.gen_expr(s[1]))
            elif tag == "if":
                cond = self.gen_expr(s[1])
                l_else = self.new_label()
                self.emit("ifFalse", cond, "", l_else)
                self.gen(s[2])
                if s[3] is None:
                    self.emit("label", "", "", l_else)
                else:
                    l_end = self.new_label()
                    self.emit("goto", "", "", l_end)
                    self.emit("label", "", "", l_else)
                    self.gen(s[3])
                    self.emit("label", "", "", l_end)
            elif tag == "while":
                l_start, l_end = self.new_label(), self.new_label()
                self.emit("label", "", "", l_start)
                cond = self.gen_expr(s[1])
                self.emit("ifFalse", cond, "", l_end)
                self.gen(s[2])
                self.emit("goto", "", "", l_start)
                self.emit("label", "", "", l_end)

    def tac_lines(self):
        for op, a1, a2, res in self.quads:
            if op == "label":
                yield f"{res}:"
            elif op == "=":
                yield f"    {res} = {a1}"
            elif op == "goto":
                yield f"    goto {res}"
            elif op == "ifFalse":
                yield f"    ifFalse {a1} goto {res}"
            elif op == "print":
                yield f"    print {a1}"
            else:
                yield f"    {res} = {a1} {op} {a2}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab4_icg.py <filename>")
        sys.exit(1)
    try:
        tree = parse_file(sys.argv[1])
    except SyntaxError as e:
        sys.exit(str(e))
    sa = analyze(tree)
    if sa.errors:
        print("\n".join(sa.errors))
        sys.exit("\nRESULT: Code not generated because of semantic errors")
    cg = CodeGenerator()
    cg.gen(tree)
    print("Three-Address Code")
    print("------------------")
    print("\n".join(cg.tac_lines()))
    print("\nQuadruples")
    print("----------")
    print(f"{'#':<4}{'op':<10}{'arg1':<10}{'arg2':<10}{'result'}")
    for i, (op, a1, a2, res) in enumerate(cg.quads):
        print(f"{i:<4}{op:<10}{a1:<10}{a2:<10}{res}")

