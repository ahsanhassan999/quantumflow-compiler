# QuantumFlow Compiler Construction: Final Project Report & Proposal
**Course:** Compiler Construction (CS)  
**Project Title:** QuantumFlow: A State-Transition Custom Programming Language & 5-Stage Interactive Web Compiler Pipeline  
**Document Generated:** [`QuantumFlow_Project_Report_4Pages.docx`](file:///d:/CC%20Project/QuantumFlow_Project_Report_4Pages.docx)  
**Page Count:** Exactly 4 Pages (Submission-Ready Word Document)

---

## 👥 Group Identification Details
| Sr. | Student Name | Roll / Seat Number | Assigned Project Role |
|:---:|:---|:---:|:---|
| **1** | **Syed Ahsan Hassan Rizvi** | **EB-24210006096** | **Group Leader & Compiler Architect** |
| **2** | **Sami Ur Rehman** | **EB-24210006086** | **Group Member & Syntax/Semantic Developer** |
| **3** | **M. Behroz Abid** | **EB-24210006001** | **Group Member & ICG / Engine Integrator** |

---

## 📄 Structure of the 4-Page Document

### **Page 1: Project Title, Proposal, Objectives, Scope & Group Details**
- **Formal Title Banner**: QuantumFlow Compiler Construction Project & Proposal.
- **Group Details Table**: Clear list of all 3 group members with roll numbers and designated roles.
- **Problem Statement & Proposal**: Explaining the transition from opaque monolithic command-line compilers to an interactive, modular web demonstrator.
- **Key Objectives & Scope**:
  - Custom non-C syntax design.
  - Formulating an unambiguous, left-recursion-free Context-Free Grammar (CFG).
  - Building 4 independent engines (Lexical, Syntax, Semantic, ICG).
  - Web IDE with live auto-completion, dark/light themes, authentication, and persistent audit logs.

---

### **Page 2: Language Design, Vocabulary & Context-Free Grammar (CFG)**
- **Language Design Philosophy**: Conceptual basis of QuantumFlow around computational state transitions.
- **Keyword & Operator Mapping Table**:
  - `int` (Integer), `pulse` (Boolean), `wave` (String)
  - `module` (Function), `initiate ... end` (Block scope)
  - `when / otherwise` (If/Else), `cycle` (While loop)
  - `show` (Print), `yield` (Return)
  - Custom combinators: `:=`, `==?`, `!=?`, `>>>`, `<<<`, `.+..`, `.-.`, `.*.`, `./.`, `&&&`, `|||`
- **Formal EBNF Grammar Box**:
  - Full production rules for `Program`, `Statement`, `ModuleDef`, `Block`, `VarAssign`, `WhenStmt`, `CycleStmt`, and operator precedence hierarchy.

---

### **Page 3: Compiler Architecture, 4 Independent Engines & Audit Logging**
- **Modular Pipeline Architecture**:
  - **Engine 1: Lexical Analyzer** (`lexer.py` / `lab1_lexer.py`) — Regex-based deterministic token scanning.
  - **Engine 2: Syntax Analyzer** (`parser.py` / `lab2_parser.py`) — Recursive descent parser outputting the AST.
  - **Engine 3: Semantic Analyzer** (`semantic.py` / `lab3_semantic.py`) — Scoped symbol table and multi-error collector.
  - **Engine 4: Intermediate Code Generator** (`icg.py` / `lab4_icg.py`) — Linear Three-Address Code and Quadruples table generator.
- **In-Browser IDE Features**:
  - CodeMirror code editor with real-time QuantumFlow auto-completion (`Ctrl + Space`).
  - Active line highlighting, line numbers, and bracket matching.
  - VS Code & Antigravity Dark and Light theme switcher.
- **Authentication & Action Audit Logging System**:
  - SQLite database (`database.py` / `compiler_logs.db`).
  - Pre-seeded accounts for group members and evaluators.
  - Records who executed what engine with timestamps, status, code snippet, and diagnostic messages.

---

### **Page 4: Test Cases, Experimental Results, Repository & Conclusion**
- **Test Benchmarks Table**:
  - `valid.txt`: Positive test proving full AST, 5-variable symbol table, 23 quadruples, and console execution.
  - `lexical_error.txt`: Demonstrates character fault injection (`@`, `$`).
  - `syntax_error.txt`: Demonstrates missing semicolon syntax error reporting.
  - `semantic_error.txt`: Demonstrates multi-error reporting (5 distinct scope and type violations).
- **Generated Three-Address Code Preview**:
  - Sample 3AC instructions showcasing register allocation (`t1`, `t2`, `t3`) and control flow labels (`L1`, `L2`, `L3`).
- **Submission Information**:
  - **GitHub Repository**: `https://github.com/ahsanhassan999/quantumflow-compiler`
  - Automated deployment config for Render (`requirements.txt`, `Procfile`).
  - Academic conclusion summarizing compliance with Compiler Construction criteria.

---

### How to Access & Submit:
You can find the generated file ready for printing or digital submission at:
👉 **[`d:\CC Project\QuantumFlow_Project_Report_4Pages.docx`](file:///d:/CC%20Project/QuantumFlow_Project_Report_4Pages.docx)**
