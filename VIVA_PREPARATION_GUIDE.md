# QuantumFlow Compiler: Viva & Presentation Preparation Guide
**Course:** Compiler Construction (CS)  
**Language Name:** QuantumFlow  
**Group Members:**
1. **Syed Ahsan Hassan Rizvi (EB-24210006096)** — *Group Leader*
2. **Sami Ur Rehman (EB-24210006086)** — *Group Member*
3. **M. Behroz Abid (EB-24210006001)** — *Group Member*

---

## 🎯 1. The 30-Second Elevator Pitch (Start with this if asked "What is your project?")

> *"Sir, our project is **QuantumFlow**, a custom-designed programming language and an interactive web-based compiler demonstrator. Instead of running as a black box, our compiler breaks down the execution process into **4 completely independent engines**: Lexical Analysis, Syntax Analysis, Semantic Analysis, and Intermediate Code Generation (Three-Address Code), followed by a runtime virtual machine. Our web interface includes an in-browser IDE with intelligent auto-completion, VS Code dark/light modes, user authentication, and persistent audit logs that track exactly which user executed which engine with timestamps."*

---

## 🧠 2. Core Viva Questions & Easy Answers

### Q1: What makes your language "QuantumFlow" unique?
**Answer:**
> *"Sir, unlike C or Java which use standard keywords, QuantumFlow is built around the idea of **state transitions**. Every keyword represents a phase of computation:
> - `initiate ... end` marks the entry point and block boundaries.
> - `module` declares a reusable block (function).
> - `when` and `otherwise` handle conditional decisions (if/else).
> - `cycle` handles iterations (while loop).
> - `show` and `yield` handle printing and returning values.
> - Data types are `int` (integers), `pulse` (booleans: true/false), and `wave` (strings).
> - We also use distinct multi-character operators like `:=` for assignment, `==?` and `!=?` for equality checks, `>>>` and `<<<` for comparisons, and `.+..`, `.-.`, `.*.`, `./.` for arithmetic so that control symbols and math symbols are never confused."*

---

### Q2: How does your Lexer (Lab 1 / Engine 1) work?
**Answer:**
> *"Sir, the Lexer converts raw source code into a linear sequence of **Tokens**. 
> - We use regular expressions mapped in a specific priority order. Longer multi-character operators like `==?` or `:=` are checked before single symbols to avoid partial matching.
> - It tracks the **line number** and **column number** of every token.
> - Whitespace and comments (`#...`) are ignored.
> - If an unrecognized character like `@` or `$` appears, it catches it immediately as a **Lexical Error** specifying the exact line and column instead of crashing."*

---

### Q3: What parser algorithm did you use in Lab 2 / Engine 2, and why?
**Answer:**
> *"Sir, we implemented a **Recursive Descent Parser**, which is a top-down parsing technique.
> - In our grammar, every non-terminal rule (like `expr`, `arith`, `term`, `factor`) is directly mapped to a Python function.
> - We eliminated **left recursion** in our expressions by structuring them into three levels: `arith` for addition/subtraction, `term` for multiplication/division, and `factor` for numbers, variables, and parentheses.
> - This naturally enforces **operator precedence** so that multiplication (`.*.`) is placed deeper in the parse tree than addition (`.+..`)."*

---

### Q4: How does your Semantic Analyzer (Lab 3 / Engine 3) work?
**Answer:**
> *"Sir, the Syntax analyzer only checks structure, but Semantic analysis checks **meaning and rules**:
> 1. **Symbol Table**: We store every variable's name, type (`int`, `pulse`, `wave`), line of declaration, and scope.
> 2. **Rule Enforcement**:
>    - A variable cannot be declared twice in the same scope.
>    - A variable must be declared before use.
>    - Type compatibility: You cannot assign an `int` to a `pulse` (boolean) variable.
>    - Arithmetic operands must both be `int`.
>    - Condition inside `when` and `cycle` must evaluate to `pulse` (boolean).
> 3. **Non-stopping Diagnostics**: Instead of stopping on the first error, we collect all errors in a list and display them all at once at the end."*

---

### Q5: What is Intermediate Code Generation (Lab 4 / Engine 4), and what are Quadruples?
**Answer:**
> *"Sir, Intermediate Code is a machine-independent representation of the program. We generate **Three-Address Code (3AC)**.
> - In 3AC, each instruction has at most one operator and two operands, utilizing temporary registers (`t1`, `t2`, etc.) and labels (`L1`, `L2`, etc.) for jumps (`goto`, `ifFalse`).
> - We also generate a **Quadruple Table**, which stores every instruction as a tuple of 4 fields: `(op, arg1, arg2, result)`. For example, `t1 = b .*. 2` is represented as `op='.*.', arg1='b', arg2='2', result='t1'`.
> - If any semantic error is found, the compiler suppresses ICG generation."*

---

### Q6: Why did you make the engines independent in the web app?
**Answer:**
> *"Sir, in our web app, each of the 4 engines has its own dedicated backend route (`/engine/lexical`, `/engine/syntax`, `/engine/semantic`, `/engine/icg`). 
> This allows an evaluator or student to test any single phase in isolation—for example, scanning tokens without parsing, or checking the symbol table without running code—or run the full pipeline together."*

---

### Q7: What is the purpose of the Login and Audit Log system?
**Answer:**
> *"Sir, we integrated a SQLite database (`compiler_logs.db`) with role-based authentication (`Group Leader`, `Group Member`, `Evaluator/Sir`). 
> Every single time an engine or pipeline is triggered, the system records **who ran it**, **what action they performed**, **timestamp**, **success/error status**, and **a snippet of the code**. This provides transparency and proof of testing."*

---

## 🔍 3. Quick Reference: The 4 Labs and Their Exact Commands

If Sir asks you to run the labs in terminal or PowerShell during viva, run these:

### **Lab 1: Lexer**
```bash
cd "d:\CC Project\labs"
python lab1_lexer.py valid.txt
python lab1_lexer.py lexical_error.txt
```
👉 *Explain: "Here valid.txt produces 74 tokens with types and lines. lexical_error.txt catches the illegal character '@' at line 3."*

### **Lab 2: Parser**
```bash
python lab2_parser.py valid.txt
python lab2_parser.py syntax_error.txt
```
👉 *Explain: "valid.txt outputs the indented parse tree with operator precedence. syntax_error.txt detects the missing semicolon on line 3."*

### **Lab 3: Semantic Analyzer**
```bash
python lab3_semantic.py valid.txt
python lab3_semantic.py semantic_error.txt
```
👉 *Explain: "valid.txt builds the symbol table with zero errors. semantic_error.txt catches all 5 errors across lines 2, 4, 5, 6, and 7 without crashing prematurely."*

### **Lab 4: Intermediate Code Generation (ICG)**
```bash
python lab4_icg.py valid.txt
python lab4_icg.py semantic_error.txt
```
👉 *Explain: "valid.txt prints linear Three-Address Code with t1, t2 registers and the 23-row Quadruples Table. On semantic_error.txt, code generation is blocked."*

---

## 💻 4. Running the Web Application Live

To start the web application:
```bash
cd "d:\CC Project"
python app.py
```
Open **`http://127.0.0.1:5000`** in browser.

### Key Points to Show Sir on the Screen:
1. **Section 1: Grammar Definition**: Show the formal CFG rules and vocabulary table at the top.
2. **Section 2: Code Editor**: Type `wh...` or `in...` to show real-time **auto-completion**.
3. **Independent Engine Buttons**: Click `1. Lexical`, `2. Syntax`, `3. Semantic`, and `4. ICG` one by one.
4. **Theme Toggle**: Click the Moon/Sun icon to show VS Code Dark and Light mode.
5. **Action Logs**: Click **"Action Logs"** to display the audit table recording user actions and timestamps.
