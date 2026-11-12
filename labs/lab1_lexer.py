"""
Compiler Construction - Lab 1: Lexical Analysis (Scanner / Tokenizer)
Language Name: QuantumFlow

Objective:
Reads a QuantumFlow source code file from command-line arguments and outputs:
1. A formatted token list (Token Index, Token Type, Lexeme, Line Number, Column Number)
2. Total token count and category summary
3. Accurate error reporting (Lexical Error with line & column number for unrecognized characters)
"""

import re
import sys

# ---- QuantumFlow Custom Keywords Table -----------------------------------
KEYWORDS = {
    "int": "INT",           # integer data type
    "pulse": "BOOL",        # boolean data type
    "wave": "STRING",       # string data type
    "module": "MODULE",     # function / reusable block
    "initiate": "INITIATE", # block start
    "end": "END",           # block end
    "when": "IF",           # if condition
    "otherwise": "ELSE",    # else branch
    "cycle": "WHILE",       # while loop
    "show": "PRINT",        # print statement
    "yield": "RETURN",      # return statement
    "true": "TRUE",         # boolean true
    "false": "FALSE"        # boolean false
}

# ---- Token Regular Expression Specifications -----------------------------
# Note: Multi-character custom operators are matched before single characters
TOKEN_SPEC = [
    # Custom Relational & Assignment Operators
    ("OP_ASSIGN",   r":="),               # Assignment :=
    ("OP_EQ",       r"==\?"),             # Equality check ==?
    ("OP_NEQ",      r"!=\?"),             # Not equal !=?
    ("OP_GT",       r">>>"),              # Greater than >>>
    ("OP_LT",       r"<<<"),              # Less than <<<
    
    # Custom Arithmetic Operators
    ("OP_ADD",      r"\.\+\."),           # Addition .+.
    ("OP_SUB",      r"\.-\."),           # Subtraction .-.
    ("OP_MUL",      r"\.\*\."),           # Multiplication .*.
    ("OP_DIV",      r"\.\/\."),           # Division ./.
    
    # Custom Logical Operators
    ("OP_AND",      r"&&&"),              # Logical AND &&&
    ("OP_OR",       r"\|\|\|"),           # Logical OR |||
    
    # Literals
    ("NUM",         r"\d+(\.\d+)?"),      # Numeric literal (integer / float)
    ("STR",         r'"[^"\n]*"'),        # String literal with double quotes
    
    # Identifiers
    ("ID",          r"[A-Za-z_]\w*"),     # Variable or function identifier
    
    # Delimiters and Punctuations
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("COLON",       r":"),
    ("SEMICOLON",   r";"),
    ("COMMA",       r","),
    
    # Comments, Newlines, and Whitespace
    ("COMMENT",     r"#.*"),              # Single-line comment starting with #
    ("NL",          r"\n"),               # Newline
    ("SKIP",        r"[ \t\r]+"),         # Whitespace to ignore
    ("BAD",         r".")                 # Unrecognized character (triggers error)
]

PATTERN = "|".join(f"(?P<{name}>{rx})" for name, rx in TOKEN_SPEC)

def tokenize(src: str):
    """
    Scans the source string and returns a list of token dictionaries:
    [{'index': i, 'type': kind, 'lexeme': text, 'line': line, 'col': col}, ...]
    Raises SyntaxError on lexical mismatch.
    """
    tokens = []
    line_num = 1
    line_start = 0
    token_index = 1
    
    for m in re.finditer(PATTERN, src):
        kind = m.lastgroup
        text = m.group()
        col_num = m.start() - line_start + 1
        
        if kind == "NL":
            line_start = m.end()
            line_num += 1
            continue
        elif kind == "SKIP" or kind == "COMMENT":
            continue
        elif kind == "BAD":
            raise SyntaxError(
                f"Lexical Error at line {line_num}, col {col_num}: unrecognized character '{text}'"
            )
        elif kind == "ID" and text in KEYWORDS:
            kind = KEYWORDS[text]
            
        tokens.append({
            "index": token_index,
            "type": kind,
            "lexeme": text,
            "line": line_num,
            "col": col_num
        })
        token_index += 1
        
    tokens.append({
        "index": token_index,
        "type": "EOF",
        "lexeme": "end of file",
        "line": line_num,
        "col": 0
    })
    return tokens

def print_token_table(tokens):
    """Prints the tokens in a clear academic table format."""
    print("==========================================================================")
    print("                  QUANTUMFLOW LEXICAL ANALYZER - LAB 1                    ")
    print("==========================================================================")
    print(f"{'#':<6}{'Token Type':<18}{'Lexeme':<22}{'Line':<8}{'Column':<8}")
    print("--------------------------------------------------------------------------")
    for t in tokens:
        print(f"{t['index']:<6}{t['type']:<18}{t['lexeme']:<22}{t['line']:<8}{t['col']:<8}")
    print("==========================================================================")
    print(f"Total Tokens Identified: {len(tokens) - 1} (+ 1 EOF marker)")
    print("RESULT: Lexical Analysis Successful (No Lexical Errors)")
    print("==========================================================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab1_lexer.py <source_file.txt>")
        print("Example: python lab1_lexer.py valid.txt")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tokens = tokenize(code)
        print_token_table(tokens)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"\n{e}")
        print("\nRESULT: Lexical Analysis FAILED")
        sys.exit(1)

