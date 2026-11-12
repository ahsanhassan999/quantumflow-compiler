# Lab 2 - Syntax Analysis (recursive descent parser) for QuantumFlow
import re
import sys

# ---- QuantumFlow Custom Keywords ----------------------------------------
KEYWORDS = {
    "int": "INT",
    "pulse": "BOOL",
    "wave": "STRING",
    "when": "IF",
    "otherwise": "ELSE",
    "cycle": "WHILE",
    "show": "PRINT",
    "true": "TRUE",
    "false": "FALSE"
}
# -------------------------------------------------------------------------

TOKEN_SPEC = [
    ("NUM", r"\d+"),
    ("STR", r'"[^"\n]*"'),
    ("OP_ASSIGN", r":="),
    ("OP_EQ", r"==\?"),
    ("OP_NEQ", r"!=\?"),
    ("OP_GT", r">>>"),
    ("OP_LT", r"<<<"),
    ("OP_ADD", r"\.\+\."),
    ("OP_SUB", r"\.-\."),
    ("OP_MUL", r"\.\*\."),
    ("OP_DIV", r"\.\/\."),
    ("ID", r"[A-Za-z_]\w*"),
    ("PUNCT", r"[(){};]"),
    ("NL", r"\n"),
    ("SKIP", r"[ \t\r]+"),
    ("BAD", r".")
]

PATTERN = "|".join(f"(?P<{name}>{rx})" for name, rx in TOKEN_SPEC)

def tokenize(src):
    """Lab 1 lexer: returns a list of (kind, lexeme, line)."""
    tokens, line = [], 1
    for m in re.finditer(PATTERN, src):
        kind, text = m.lastgroup, m.group()
        if kind == "NL":
            line += 1
        elif kind == "SKIP":
            continue
        elif kind == "BAD":
            raise SyntaxError(f"Lexical Error at line {line}: unknown character '{text}'")
        elif kind == "ID" and text in KEYWORDS:
            tokens.append((KEYWORDS[text], text, line))
        elif kind.startswith("OP_") or kind == "PUNCT":
            tokens.append((text, text, line))
        else:
            tokens.append((kind, text, line))
    tokens.append(("EOF", "end of file", line))
    return tokens

class Parser:
    """One method per non-terminal of the grammar."""
    def __init__(self, tokens):
        self.toks, self.pos = tokens, 0

    def peek(self):
        return self.toks[self.pos][0]

    def match(self, kind):
        tok = self.toks[self.pos]
        if tok[0] != kind:
            raise SyntaxError(f"Syntax Error at line {tok[2]}: expected '{kind}' but found '{tok[1]}'")
        self.pos += 1
        return tok

    # program -> stmt_list EOF
    def program(self):
        body = self.stmt_list()
        self.match("EOF")
        return body

    # stmt_list -> stmt stmt_list | epsilon
    def stmt_list(self):
        stmts = []
        while self.peek() not in ("EOF", "}"):
            stmts.append(self.stmt())
        return stmts

    # stmt -> decl | assign | if_stmt | while_stmt | print_stmt
    def stmt(self):
        kind, text, line = self.toks[self.pos]
        if kind in ("INT", "BOOL", "STRING"):          # decl -> type ID (':=' expr)? ';'
            self.pos += 1
            name, init = self.match("ID")[1], None
            if self.peek() == ":=":
                self.match(":=")
                init = self.expr()
            self.match(";")
            return ("decl", text, name, init, line)
        if kind == "ID":                               # assign -> ID ':=' expr ';'
            self.pos += 1
            self.match(":=")
            value = self.expr()
            self.match(";")
            return ("assign", text, value, line)
        if kind == "IF":                               # if_stmt -> IF '(' expr ')' block (ELSE block)?
            self.pos += 1
            self.match("(")
            cond = self.expr()
            self.match(")")
            then, other = self.block(), None
            if self.peek() == "ELSE":
                self.pos += 1
                other = self.block()
            return ("if", cond, then, other, line)
        if kind == "WHILE":                            # while_stmt -> WHILE '(' expr ')' block
            self.pos += 1
            self.match("(")
            cond = self.expr()
            self.match(")")
            return ("while", cond, self.block(), line)
        if kind == "PRINT":                            # print_stmt -> PRINT '(' expr ')' ';'
            self.pos += 1
            self.match("(")
            value = self.expr()
            self.match(")")
            self.match(";")
            return ("print", value, line)
        raise SyntaxError(f"Syntax Error at line {line}: a statement cannot start with '{text}'")

    # block -> '{' stmt_list '}'
    def block(self):
        self.match("{")
        body = self.stmt_list()
        self.match("}")
        return body

    # expr -> arith (relop arith)?
    def expr(self):
        left = self.arith()
        if self.peek() in ("<<<", ">>>", "==?", "!=?"):
            op, _, line = self.toks[self.pos]
            self.pos += 1
            left = ("binop", op, left, self.arith(), line)
        return left

    # arith -> term (('.+.' | '.-.') term)*
    def arith(self):
        left = self.term()
        while self.peek() in (".+.", ".-."):
            op, _, line = self.toks[self.pos]
            self.pos += 1
            left = ("binop", op, left, self.term(), line)
        return left

    # term -> factor (('.*.' | './.') factor)*
    def term(self):
        left = self.factor()
        while self.peek() in (".*.", "./."):
            op, _, line = self.toks[self.pos]
            self.pos += 1
            left = ("binop", op, left, self.factor(), line)
        return left

    # factor -> NUM | STR | TRUE | FALSE | ID | '(' expr ')'
    def factor(self):
        kind, text, line = self.toks[self.pos]
        self.pos += 1
        if kind == "NUM":
            return ("num", text, line)
        if kind == "STR":
            return ("str", text, line)
        if kind in ("TRUE", "FALSE"):
            return ("bool", text, line)
        if kind == "ID":
            return ("id", text, line)
        if kind == "(":
            inner = self.expr()
            self.match(")")
            return inner
        raise SyntaxError(f"Syntax Error at line {line}: expected an expression but found '{text}'")

def show_tree(node, depth=0):
    pad = "  " * depth
    if isinstance(node, list):
        for n in node:
            show_tree(n, depth)
        return
    tag = node[0]
    if tag == "decl":
        print(f"{pad}Declaration: {node[1]} {node[2]}")
        if node[3]:
            show_tree(node[3], depth + 1)
    elif tag == "assign":
        print(f"{pad}Assignment: {node[1]}")
        show_tree(node[2], depth + 1)
    elif tag == "if":
        print(f"{pad}If")
        print(f"{pad}  Condition")
        show_tree(node[1], depth + 2)
        print(f"{pad}  Then")
        show_tree(node[2], depth + 2)
        if node[3] is not None:
            print(f"{pad}  Else")
            show_tree(node[3], depth + 2)
    elif tag == "while":
        print(f"{pad}While")
        print(f"{pad}  Condition")
        show_tree(node[1], depth + 2)
        print(f"{pad}  Body")
        show_tree(node[2], depth + 2)
    elif tag == "print":
        print(f"{pad}Print")
        show_tree(node[1], depth + 1)
    elif tag == "binop":
        print(f"{pad}Operator: {node[1]}")
        show_tree(node[2], depth + 1)
        show_tree(node[3], depth + 1)
    else:
        print(f"{pad}{tag.capitalize()}: {node[1]}")

def parse_file(path):
    return Parser(tokenize(open(path).read())).program()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab2_parser.py <filename>")
        sys.exit(1)
    try:
        tree = parse_file(sys.argv[1])
        print("Parse Tree")
        print("----------")
        show_tree(tree)
        print("\nRESULT: Syntax is correct")
    except SyntaxError as e:
        print(e)
        print("\nRESULT: Syntax is NOT correct")

