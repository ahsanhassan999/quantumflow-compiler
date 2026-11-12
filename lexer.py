"""
Lexical Analyzer (Scanner) for QuantumFlow Programming Language.
Breaks raw source code into a sequence of structured Tokens.
"""

import re
from typing import List, NamedTuple, Optional

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

# QuantumFlow language specification tokens
# Note: Longer operators must come before shorter ones to prevent partial matching (e.g. '==?' before '=')
TOKEN_SPECIFICATION = [
    # Custom Operators
    ('OP_EQ',       r'==\?'),              # Equality check ==?
    ('OP_NEQ',      r'!=\?'),              # Not equal !=?
    ('OP_ASSIGN',   r':='),                # Assignment :=
    ('OP_ADD',      r'\.\+\.'),            # Addition .+.
    ('OP_SUB',      r'\.-\.'),            # Subtraction .-.
    ('OP_MUL',      r'\.\*\.'),            # Multiplication .*.
    ('OP_DIV',      r'\.\/\.'),            # Division ./.
    ('OP_AND',      r'&&&'),               # Logical AND &&&
    ('OP_OR',       r'\|\|\|'),            # Logical OR |||
    ('OP_GT',       r'>>>'),               # Greater than >>>
    ('OP_LT',       r'<<<'),               # Less than <<<
    
    # Delimiters and Punctuations
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('COLON',       r':'),
    ('COMMA',       r','),
    
    # Literals
    ('NUMBER',      r'\d+(\.\d+)?'),
    ('STRING',      r'"[^"\n]*"'),
    
    # Identifiers & Keywords
    ('IDENTIFIER',  r'[a-zA-Z_][a-zA-Z0-9_]*'),
    
    # Whitespace & Comments
    ('COMMENT',     r'#.*'),
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t\r]+'),
    ('MISMATCH',    r'.'),                 # Any unexpected character
]

# QuantumFlow custom keywords
KEYWORDS = {
    'initiate':   'KW_INITIATE',   # marks entry point / block start
    'when':       'KW_WHEN',       # if
    'otherwise':  'KW_OTHERWISE',  # else
    'module':     'KW_MODULE',     # function
    'yield':      'KW_YIELD',      # return
    'cycle':      'KW_CYCLE',      # while loop
    'show':       'KW_SHOW',       # print built-in
    'end':        'KW_END',        # block end closure
}

def tokenize(code: str) -> List[Token]:
    """
    Scans the source code and returns a list of Token objects.
    Throws SyntaxError on invalid/unrecognized characters.
    """
    tokens = []
    line_num = 1
    line_start = 0
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    
    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1
        
        if kind == 'NEWLINE':
            line_start = match.end()
            line_num += 1
            continue
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Lexical Error: Unrecognized character '{value}' at line {line_num}, column {column}")
        elif kind == 'IDENTIFIER':
            # Check if this identifier is a reserved keyword in QuantumFlow
            if value in KEYWORDS:
                kind = KEYWORDS[value]
        
        tokens.append(Token(kind, value, line_num, column))
        
    tokens.append(Token('EOF', '', line_num, 0))
    return tokens

