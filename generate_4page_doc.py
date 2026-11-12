"""
Generate a concise, professional 4-page Project Proposal and Final Report Word Document.
Pages strictly structured:
Page 1: Project Title, Proposal, Objectives, Scope & Group Details
Page 2: QuantumFlow Language Design, Vocabulary Table & Context-Free Grammar (CFG)
Page 3: Architecture of 4 Independent Compiler Engines, Web IDE & User Audit Logging
Page 4: Test Cases, Experimental Results, Verification, GitHub Repository & Conclusion
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(level=level)
    h.paragraph_format.space_before = Pt(6)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Arial'
    if level == 1:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)
    else:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
    return h

def add_code_box(doc, text, font_size=8):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(30, 41, 59)

doc = docx.Document()

# Set concise 0.65 inch margins to comfortably fit 4 pages
for section in doc.sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

# ==============================================================================
# PAGE 1: PROJECT COVER, PROPOSAL, OBJECTIVES & GROUP DETAILS
# ==============================================================================
header_tbl = doc.add_table(rows=1, cols=1)
header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
h_cell = header_tbl.cell(0, 0)
set_cell_background(h_cell, "0F4C81")
set_cell_margins(h_cell, top=120, bottom=120, left=150, right=150)
hp = h_cell.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
hrun1 = hp.add_run("COMPILER CONSTRUCTION PROJECT FILE & PROPOSAL\n")
hrun1.font.name = 'Arial'
hrun1.font.size = Pt(14)
hrun1.font.bold = True
hrun1.font.color.rgb = RGBColor(255, 255, 255)

hrun2 = hp.add_run("QuantumFlow: A State-Transition Custom Programming Language & 5-Stage Interactive Web Compiler Pipeline")
hrun2.font.name = 'Arial'
hrun2.font.size = Pt(10)
hrun2.font.color.rgb = RGBColor(224, 242, 254)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Group Information Table
add_heading_styled(doc, "Project Group Details", level=2)
g_table = doc.add_table(rows=4, cols=4)
g_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Sr.", "Member Name", "Roll / Seat Number", "Assigned Project Role"]
for i, h in enumerate(headers):
    c = g_table.cell(0, i)
    set_cell_background(c, "1E293B")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'Arial'
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(8.5)

group_data = [
    ("1", "Syed Ahsan Hassan Rizvi", "EB-24210006096", "Group Leader & Compiler Architect"),
    ("2", "Sami Ur Rehman", "EB-24210006086", "Group Member & Syntax/Semantic Developer"),
    ("3", "M. Behroz Abid", "EB-24210006001", "Group Member & ICG / Engine Integrator")
]
for row_idx, rvals in enumerate(group_data, start=1):
    bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(rvals):
        c = g_table.cell(row_idx, col_idx)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        if col_idx in (0, 2):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if col_idx == 1:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Project Proposal Section
add_heading_styled(doc, "1. Project Proposal & Problem Statement", level=1)
p_prop = doc.add_paragraph()
p_prop.paragraph_format.space_after = Pt(3)
p_prop.paragraph_format.line_spacing = 1.15
r = p_prop.add_run(
    "Standard compiler construction projects are often monolithic scripts that run as opaque command-line tools, "
    "making it difficult for evaluators and students to inspect the exact state transformations across compilation stages. "
    "This project proposes QuantumFlow, a purpose-built programming language modeling state transitions, accompanied by an "
    "interactive, web-based compiler demonstrator. The system decomposes the compilation process into four decoupled, independent "
    "engines (Lexical, Syntax, Semantic, and Intermediate Code Generation) plus a runtime execution evaluator. "
    "The application provides a formal grammar viewer, intelligent in-browser IDE with auto-completion, role-based authentication, "
    "and persistent audit logging to record who executed what compilation engine with exact timestamps."
)
r.font.name = 'Arial'
r.font.size = Pt(8.5)

# Objectives & Scope
add_heading_styled(doc, "2. Key Objectives & Scope", level=1)
p_obj = doc.add_paragraph()
p_obj.paragraph_format.space_after = Pt(2)
p_obj.paragraph_format.line_spacing = 1.15
r_obj = p_obj.add_run(
    "• Language Design: Formulate custom keywords and multi-character operators avoiding C-family keywords.\n"
    "• Grammar Definition: Establish an unambiguous Context-Free Grammar (CFG) in EBNF without left recursion.\n"
    "• Independent Engines: Provide 4 isolated engines that can be triggered individually or as a complete pipeline.\n"
    "• Robust Error Diagnostics: Catch and pinpoint lexical characters, syntax tokens, and semantic scope violations.\n"
    "• Web Demonstrator & Logging: Deliver a modern VS Code/Antigravity dark & light themed interface with user session management and activity audit tracking."
)
r_obj.font.name = 'Arial'
r_obj.font.size = Pt(8.5)

# ==============================================================================
# PAGE 2: LANGUAGE DESIGN, VOCABULARY & CONTEXT-FREE GRAMMAR
# ==============================================================================
doc.add_page_break()

add_heading_styled(doc, "3. QuantumFlow Language Specification", level=1)
p_spec = doc.add_paragraph()
p_spec.paragraph_format.space_after = Pt(3)
p_spec.paragraph_format.line_spacing = 1.1
r_spec = p_spec.add_run(
    "QuantumFlow replaces traditional keywords with computation-phase combinators (initiation, decision, iteration, and return). "
    "Multi-character symbols (e.g. :=, ==?, >>>, .+.) provide unmistakable visual distinction between control and arithmetic."
)
r_spec.font.name = 'Arial'
r_spec.font.size = Pt(8.5)

# Vocabulary Mapping Table
add_heading_styled(doc, "Table 1: Language Keywords and Custom Operators", level=2)
v_table = doc.add_table(rows=11, cols=4)
v_table.alignment = WD_TABLE_ALIGNMENT.CENTER
v_headers = ["Standard Keyword", "QuantumFlow Keyword", "Token Class", "Operational Semantic"]
for i, h in enumerate(v_headers):
    c = v_table.cell(0, i)
    set_cell_background(c, "0F4C81")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'Arial'
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(8)

vocab_rows = [
    ("int (integer)", "int", "INT", "Signed 32-bit integer primitive"),
    ("bool (boolean)", "pulse", "BOOL", "Logical boolean flag (true / false)"),
    ("string", "wave", "STRING", "Quoted text sequence literal"),
    ("function", "module", "MODULE", "Reusable subprogram definition"),
    ("begin / start", "initiate", "INITIATE", "Entry point & block boundary opener"),
    ("end", "end", "END", "Block scope closer"),
    ("if / else", "when / otherwise", "IF / ELSE", "Dual-alternative conditional branching"),
    ("while loop", "cycle", "WHILE", "Pre-tested iterative loop construct"),
    ("print / return", "show / yield", "PRINT / RETURN", "Console emission and value return"),
    ("assignment", ":=", "OP_ASSIGN", "State assignment combinator")
]
for r_i, r_data in enumerate(vocab_rows, start=1):
    bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
    for c_i, val in enumerate(r_data):
        c = v_table.cell(r_i, c_i)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = 'Arial'
        r.font.size = Pt(7.5)
        if c_i in (0, 2):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if c_i == 1:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Formal Grammar (CFG)
add_heading_styled(doc, "4. Formal Context-Free Grammar (CFG / EBNF)", level=1)
p_cfg_desc = doc.add_paragraph()
p_cfg_desc.paragraph_format.space_after = Pt(2)
r_cd = p_cfg_desc.add_run(
    "The grammar is structured in Extended Backus-Naur Form (EBNF) specifically designed to eliminate left-recursion, "
    "enabling single-pass deterministic recursive descent parsing with operator precedence (multiplication before addition)."
)
r_cd.font.name = 'Arial'
r_cd.font.size = Pt(8.5)

cfg_code = """Program        ::= ( Statement )*
Statement      ::= ModuleDef | VarAssign | WhenStmt | CycleStmt | YieldStmt | ShowStmt | Block
ModuleDef      ::= "module" IDENTIFIER "(" [ ParamList ] ")" ":" Block
ParamList      ::= IDENTIFIER ( "," IDENTIFIER )*
Block          ::= "initiate" Statement* [ "end" ]
VarAssign      ::= IDENTIFIER ":=" Expr
WhenStmt       ::= "when" Expr Block [ "otherwise" Block ]
CycleStmt      ::= "cycle" Expr Block
YieldStmt      ::= "yield" Expr
ShowStmt       ::= "show" "(" Expr ")"
Expr           ::= LogicalOr
LogicalOr      ::= LogicalAnd ( "|||" LogicalAnd )*
LogicalAnd     ::= Relational ( "&&&" Relational )*
Relational     ::= Additive [ ( "==?" | "!=?" | ">>>" | "<<<" ) Additive ]
Additive       ::= Multiplicative ( ( ".+." | ".-." ) Multiplicative )*
Multiplicative ::= Primary ( ( ".*." | "./." ) Primary )*
Primary        ::= NUMBER | STRING | IDENTIFIER | true | false | "(" Expr ")" """
add_code_box(doc, cfg_code, font_size=7.5)

# ==============================================================================
# PAGE 3: SYSTEM ARCHITECTURE & 4 INDEPENDENT ENGINES
# ==============================================================================
doc.add_page_break()

add_heading_styled(doc, "5. Compiler Pipeline Architecture & Independent Engines", level=1)
p_arch = doc.add_paragraph()
p_arch.paragraph_format.space_after = Pt(3)
p_arch.paragraph_format.line_spacing = 1.15
r_arch = p_arch.add_run(
    "The QuantumFlow compiler architecture separates concerns into four autonomous stages, accessible both via command-line "
    "scripts (`labs/` folder) and through dedicated REST API endpoints (`/engine/<stage>`) on the Flask web application:"
)
r_arch.font.name = 'Arial'
r_arch.font.size = Pt(8.5)

# Engine Breakdown Table
e_table = doc.add_table(rows=5, cols=4)
e_table.alignment = WD_TABLE_ALIGNMENT.CENTER
e_headers = ["Compiler Stage", "Underlying Module", "Algorithm & Technique", "Generated Artifact"]
for i, h in enumerate(e_headers):
    c = e_table.cell(0, i)
    set_cell_background(c, "1E293B")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'Arial'
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(8)

engines_data = [
    ("1. Lexical Analysis", "lexer.py / lab1_lexer.py", "Regex Deterministic Scanning", "Token Stream (Type, Lexeme, Line, Col)"),
    ("2. Syntax Analysis", "parser.py / lab2_parser.py", "Recursive Descent Parsing", "Abstract Syntax Tree (AST) Hierarchy"),
    ("3. Semantic Analysis", "semantic.py / lab3_semantic.py", "Scoped Symbol Table & Type Inferrer", "Symbol Table + Scoped Diagnostics"),
    ("4. Intermediate Code", "icg.py / lab4_icg.py", "AST Visitor Quadruple Generator", "Three-Address Code (3AC) & Quadruples")
]
for r_i, r_data in enumerate(engines_data, start=1):
    bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
    for c_i, val in enumerate(r_data):
        c = e_table.cell(r_i, c_i)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = 'Arial'
        r.font.size = Pt(7.5)
        if c_i == 0:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Web IDE & User Audit Logging System
add_heading_styled(doc, "6. In-Browser IDE, User Roles & Audit Logging", level=1)
p_ui = doc.add_paragraph()
p_ui.paragraph_format.space_after = Pt(3)
p_ui.paragraph_format.line_spacing = 1.15
r_ui = p_ui.add_run(
    "• Intelligent Code Editor: Powered by CodeMirror with real-time QuantumFlow auto-completion (Ctrl+Space), "
    "bracket matching, line numbering, and VS Code / Antigravity dark & light mode styling.\n"
    "• User Authentication: SQLite-backed account system (`database.py`) with pre-configured accounts for group members and evaluators.\n"
    "• Persistent Audit Trails: Every trigger of an independent engine or full pipeline is recorded in `compiler_logs.db` with "
    "the username, action name, status (SUCCESS/ERROR), diagnostic summary, code preview, and exact timestamp."
)
r_ui.font.name = 'Arial'
r_ui.font.size = Pt(8.5)

# Example Audit Log Record Box
add_heading_styled(doc, "Sample Recorded Audit Log Schema", level=2)
audit_sample = """[2026-11-12 22:40:12] USER: ahsan (Group Leader) | ACTION: ENGINE_LEXICAL  | STATUS: SUCCESS | Generated 74 tokens
[2026-11-12 22:40:15] USER: instructor (Evaluator)  | ACTION: ENGINE_SYNTAX   | STATUS: SUCCESS | AST generated successfully
[2026-11-12 22:40:18] USER: instructor (Evaluator)  | ACTION: ENGINE_SEMANTIC | STATUS: ERROR   | 5 semantic error(s) detected
[2026-11-12 22:40:22] USER: sami (Group Member)     | ACTION: FULL_PIPELINE   | STATUS: SUCCESS | All 5 stages completed"""
add_code_box(doc, audit_sample, font_size=7.5)

# ==============================================================================
# PAGE 4: TEST CASES, EXPERIMENTAL RESULTS & CONCLUSION
# ==============================================================================
doc.add_page_break()

add_heading_styled(doc, "7. Experimental Verification & Test Cases", level=1)
p_test = doc.add_paragraph()
p_test.paragraph_format.space_after = Pt(2)
r_test = p_test.add_run(
    "The compiler was verified against positive benchmarks and strict fault-injection test files:"
)
r_test.font.name = 'Arial'
r_test.font.size = Pt(8.5)

# Test cases summary table
t_table = doc.add_table(rows=5, cols=4)
t_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t_headers = ["Test Benchmark", "Test Purpose", "Tested Engine", "Observed Outcome"]
for i, h in enumerate(t_headers):
    c = t_table.cell(0, i)
    set_cell_background(c, "0F4C81")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'Arial'
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(8)

test_data = [
    ("valid.txt", "Exercises all keywords, declarations, loops, arithmetic", "All 4 Engines + VM", "Full AST, Symbol Table (5 vars), 23-row Quadruples, Output: 'positive'"),
    ("lexical_error.txt", "Fault injection of illegal characters ('@', '$')", "Lexical Scanner", "Catches 'unrecognized character @ at line 3, col 13'"),
    ("syntax_error.txt", "Missing semicolon delimiter after declaration", "Parser Engine", "Catches 'expected ; but found a at line 3'"),
    ("semantic_error.txt", "Breaks 5 semantic rules (undeclared, type mismatch)", "Semantic Checker", "Reports all 5 errors across lines 2, 4, 5, 6, 7 without premature exit")
]
for r_i, r_data in enumerate(test_data, start=1):
    bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
    for c_i, val in enumerate(r_data):
        c = t_table.cell(r_i, c_i)
        set_cell_background(c, bg)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = 'Arial'
        r.font.size = Pt(7.5)
        if c_i == 0:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# 3AC Output Preview
add_heading_styled(doc, "8. Generated Intermediate Code (3AC) for Benchmark", level=1)
sample_3ac = """    a = 5                 | t2 = a .+. t1          | L1: big = false      | L3: t4 = a <<< b
    b = 10                | sum = t2               | L2:                  | ifFalse t4 goto L4
    big = false           | t3 = sum >>> 20        |                      | t5 = a .+. 1
    msg = "done"          | ifFalse t3 goto L1     |                      | a = t5
    t1 = b .*. 2          | big = true; goto L2    |                      | goto L3; L4: print sum"""
add_code_box(doc, sample_3ac, font_size=7)

# Submission Links & Conclusion
add_heading_styled(doc, "9. Submission Artifacts, Repository & Conclusion", level=1)
p_concl = doc.add_paragraph()
p_concl.paragraph_format.space_after = Pt(2)
p_concl.paragraph_format.line_spacing = 1.15
r_concl = p_concl.add_run(
    "• GitHub Repository: https://github.com/ahsanhassan999/quantumflow-compiler\n"
    "• Automated Live Deployment: Configured for Render cloud hosting via `requirements.txt` and `Procfile`.\n"
    "• Academic Deliverables: The project repository provides complete modular code for all 4 labs in `labs/`, "
    "a browser-based interactive IDE with independent engine triggers, and a comprehensive audit trail.\n\n"
    "Conclusion: QuantumFlow successfully fulfills all curricular requirements of Compiler Construction. "
    "By delivering decoupled engines, clear parse trees, rigorous type checking, and Three-Address Code with quadruples, "
    "the project provides an exceptional practical demonstration of modern compiler theory and implementation."
)
r_concl.font.name = 'Arial'
r_concl.font.size = Pt(8)

# Save Document
out_doc_name = "QuantumFlow_Project_Report_4Pages.docx"
doc.save(out_doc_name)
print("Saved 4-page Project Proposal and Final Report to:", out_doc_name)
