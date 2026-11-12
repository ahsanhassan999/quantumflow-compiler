import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import subprocess
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F6F9")
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(33, 37, 41)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_output_block(doc, output_text, is_error=False):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    bg_hex = "1E1E24" if not is_error else "2D141E"
    set_cell_background(cell, bg_hex)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.1
    run = p.add_run(output_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    if is_error:
        run.font.color.rgb = RGBColor(255, 120, 140)
    else:
        run.font.color.rgb = RGBColor(100, 255, 150)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else (res.stdout + "\n" + res.stderr)

doc = docx.Document()

# Page Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
t_run = title_p.add_run("COMPILER CONSTRUCTION LAB REPORT\nLAB 1, LAB 2, LAB 3 & LAB 4")
t_run.font.name = 'Arial'
t_run.font.size = Pt(18)
t_run.font.bold = True
t_run.font.color.rgb = RGBColor(15, 76, 129)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
s_run = sub_p.add_run("Language Name: QuantumFlow | Python Implementation & Complete Verification")
s_run.font.name = 'Arial'
s_run.font.size = Pt(11)
s_run.font.italic = True
s_run.font.color.rgb = RGBColor(100, 110, 120)

# Group Info Table
g_table = doc.add_table(rows=4, cols=3)
g_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Student Name", "Roll Number", "Project Role"]
for i, h in enumerate(headers):
    c = g_table.cell(0, i)
    set_cell_background(c, "0F4C81")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(9.5)

data = [
    ("Syed Ahsan Hassan Rizvi", "EB-24210006096", "Group Leader"),
    ("Sami Ur Rehman", "EB-24210006086", "Group Member"),
    ("M. Behroz Abid", "EB-24210006001", "Group Member")
]
for row_idx, (name, roll, role) in enumerate(data, start=1):
    bg = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate([name, roll, role]):
        c = g_table.cell(row_idx, col_idx)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(9)
        if col_idx == 0:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# Executive Summary
h1 = doc.add_heading("1. Language Design & Vocabulary Specification", level=1)
p = doc.add_paragraph("QuantumFlow is a custom language built on the principle of state transitions. Every keyword and operator has a distinct semantic identity to prevent syntactic collisions and clarify control flow.")

# Vocabulary Mapping Table
v_table = doc.add_table(rows=10, cols=4)
v_table.alignment = WD_TABLE_ALIGNMENT.CENTER
v_headers = ["Standard Keyword", "QuantumFlow Keyword", "Token Type", "Operational Description"]
for i, h in enumerate(v_headers):
    c = v_table.cell(0, i)
    set_cell_background(c, "2C3E50")
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(8.5)

vocab_data = [
    ("int", "int", "INT", "Integer primitive data type"),
    ("bool", "pulse", "BOOL", "Boolean flag data type (true / false)"),
    ("string", "wave", "STRING", "String sequence literal data type"),
    ("if", "when", "IF", "Initiates conditional branching block"),
    ("else", "otherwise", "ELSE", "Alternate conditional execution path"),
    ("while", "cycle", "WHILE", "Iterative pre-tested loop execution"),
    ("print", "show", "PRINT", "Direct output to execution stream"),
    ("assignment", ":=", "OP_ASSIGN", "Explicit custom state assignment"),
    ("equality / greater", "==? / >>>", "OP_EQ / OP_GT", "Custom non-C relational combinators")
]
for row_idx, row_vals in enumerate(vocab_data, start=1):
    bg = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row_vals):
        c = v_table.cell(row_idx, col_idx)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(8)
        if col_idx == 1:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Context-Free Grammar
doc.add_heading("2. Formal Context-Free Grammar (CFG)", level=1)
cfg_text = """program     -> stmt_list EOF
stmt_list   -> stmt stmt_list | epsilon
stmt        -> decl | assign | if_stmt | while_stmt | print_stmt
decl        -> type ID ';'  |  type ID ':=' expr ';'
type        -> int | pulse | wave
assign      -> ID ':=' expr ';'
if_stmt     -> when '(' expr ')' block [ otherwise block ]
while_stmt  -> cycle '(' expr ')' block
print_stmt  -> show '(' expr ')' ';'
block       -> '{' stmt_list '}'
expr        -> arith [ relop arith ]
relop       -> '<<<' | '>>>' | '==?' | '!=?'
arith       -> term ( ( '.+.' | '.-.' ) term )*
term        -> factor ( ( '.*.' | './.' ) factor )*
factor      -> NUM | STR | true | false | ID | '(' expr ')'"""
add_code_block(doc, cfg_text)

# Input Test Programs Section
doc.add_heading("3. Reference Test Cases Used for Verification", level=1)
doc.add_paragraph("All four labs were evaluated on standardized test files created according to lab manual specifications:")

doc.add_heading("Test 1: valid.txt (Correct program exercising all constructs)", level=2)
with open("valid.txt") as f:
    add_code_block(doc, f.read())

doc.add_heading("Test 2: lexical_error.txt (Illegal characters '@', '$')", level=2)
with open("lexical_error.txt") as f:
    add_code_block(doc, f.read())

doc.add_heading("Test 3: syntax_error.txt (Missing semicolon delimiter)", level=2)
with open("syntax_error.txt") as f:
    add_code_block(doc, f.read())

doc.add_heading("Test 4: semantic_error.txt (Violates 5 distinct semantic rules)", level=2)
with open("semantic_error.txt") as f:
    add_code_block(doc, f.read())

# ================= LAB 1 =================
doc.add_page_break()
doc.add_heading("4. LAB 1: LEXICAL ANALYSIS (SCANNER)", level=1)
doc.add_paragraph("Objective: Scan the raw QuantumFlow source code, tokenize every lexeme with its token type, line number, and column number, and detect invalid character tokens.")

doc.add_heading("Lab 1 Source Code: lab1_lexer.py", level=2)
with open("lab1_lexer.py", "r", encoding="utf-8") as f:
    add_code_block(doc, f.read())

doc.add_heading("Lab 1 Execution on valid.txt:", level=2)
out_l1_valid = run_cmd(["python", "lab1_lexer.py", "valid.txt"])
add_output_block(doc, out_l1_valid)

doc.add_heading("Lab 1 Execution on lexical_error.txt (Error Catching Proof):", level=2)
out_l1_err = run_cmd(["python", "lab1_lexer.py", "lexical_error.txt"])
add_output_block(doc, out_l1_err, is_error=True)

# ================= LAB 2 =================
doc.add_page_break()
doc.add_heading("5. LAB 2: SYNTAX ANALYSIS (RECURSIVE DESCENT PARSER)", level=1)
doc.add_paragraph("Objective: Verify grammatical correctness of the token stream using recursive descent parsing and produce an indented parse tree confirming operator precedence.")

doc.add_heading("Lab 2 Source Code: lab2_parser.py", level=2)
with open("lab2_parser.py", "r", encoding="utf-8") as f:
    add_code_block(doc, f.read())

doc.add_heading("Lab 2 Execution on valid.txt (Indented Parse Tree):", level=2)
out_l2_valid = run_cmd(["python", "lab2_parser.py", "valid.txt"])
add_output_block(doc, out_l2_valid)

doc.add_heading("Lab 2 Execution on syntax_error.txt (Error Catching Proof):", level=2)
out_l2_err = run_cmd(["python", "lab2_parser.py", "syntax_error.txt"])
add_output_block(doc, out_l2_err, is_error=True)

# ================= LAB 3 =================
doc.add_page_break()
doc.add_heading("6. LAB 3: SEMANTIC ANALYSIS (SYMBOL TABLE & TYPE CHECKER)", level=1)
doc.add_paragraph("Objective: Walk the Lab 2 parse tree to enforce scope declaration and type consistency. Collect all semantic violations across the entire program without stopping prematurely.")

doc.add_heading("Lab 3 Source Code: lab3_semantic.py", level=2)
with open("lab3_semantic.py", "r", encoding="utf-8") as f:
    add_code_block(doc, f.read())

doc.add_heading("Lab 3 Execution on valid.txt (Symbol Table Output):", level=2)
out_l3_valid = run_cmd(["python", "lab3_semantic.py", "valid.txt"])
add_output_block(doc, out_l3_valid)

doc.add_heading("Lab 3 Execution on semantic_error.txt (All 5 Errors Caught):", level=2)
out_l3_err = run_cmd(["python", "lab3_semantic.py", "semantic_error.txt"])
add_output_block(doc, out_l3_err, is_error=True)

# ================= LAB 4 =================
doc.add_page_break()
doc.add_heading("7. LAB 4: INTERMEDIATE CODE GENERATION (3AC & QUADRUPLES)", level=1)
doc.add_paragraph("Objective: Generate linear Three-Address Code (TAC) and a Quadruple Table with columns (op, arg1, arg2, result) from a verified parse tree. Suppress code generation if semantic errors exist.")

doc.add_heading("Lab 4 Source Code: lab4_icg.py", level=2)
with open("lab4_icg.py", "r", encoding="utf-8") as f:
    add_code_block(doc, f.read())

doc.add_heading("Lab 4 Execution on valid.txt (Three-Address Code & Quadruple Table):", level=2)
out_l4_valid = run_cmd(["python", "lab4_icg.py", "valid.txt"])
add_output_block(doc, out_l4_valid)

doc.add_heading("Lab 4 Execution on semantic_error.txt (Code Generation Suppressed):", level=2)
out_l4_err = run_cmd(["python", "lab4_icg.py", "semantic_error.txt"])
add_output_block(doc, out_l4_err, is_error=True)

# Save document
output_docx_path = "QuantumFlow_Compiler_Labs_Report.docx"
doc.save(output_docx_path)
print("Saved complete lab report document to:", output_docx_path)

