# Compiler Construction: Complete Lab Guide (Lab 1 – 4)
**Course:** Compiler Construction (CS)  
**Language Name:** QuantumFlow  
**Generated Document:** [`QuantumFlow_Compiler_Labs_Report.docx`](file:///d:/CC%20Project/QuantumFlow_Compiler_Labs_Report.docx)

---

## 👥 Group Details
1. **Syed Ahsan Hassan Rizvi** (EB-24210006096) — **Group Leader**
2. **Sami Ur Rehman** (EB-24210006086) — **Group Member**
3. **M. Behroz Abid** (EB-24210006001) — **Group Member**

---

## 📄 Formatted Word Document Generated!
A submission-ready Word document has been compiled and saved to your project directory:  
👉 **`d:\CC Project\QuantumFlow_Compiler_Labs_Report.docx`**

It contains:
- Complete Cover Page & Group Details Table
- QuantumFlow Vocabulary & Operator Specification
- Formal Context-Free Grammar (CFG / EBNF)
- Test Files (`valid.txt`, `lexical_error.txt`, `syntax_error.txt`, `semantic_error.txt`)
- **Full Source Code** for all 4 Labs
- **Actual Terminal Outputs** (both correct runs and error-catching proof) embedded in clean code blocks and dark terminal tables.

---

## 1. Quick Summary of the 4 Labs

| Lab | Objective | Source File | Run Command | Expected Output |
|---|---|---|---|---|
| **Lab 1** | Lexical Analysis (Scanner) | `lab1_lexer.py` | `python lab1_lexer.py valid.txt` | Formatted table of 74 tokens with Type, Lexeme, Line, and Column. |
| **Lab 2** | Syntax Analysis (Parser) | `lab2_parser.py` | `python lab2_parser.py valid.txt` | Indented Parse Tree showing operator precedence (`.*.` below `.+..`) and `RESULT: Syntax is correct`. |
| **Lab 3** | Semantic Analysis | `lab3_semantic.py` | `python lab3_semantic.py valid.txt` | Formatted Symbol Table and `RESULT: No semantic errors`. |
| **Lab 4** | Intermediate Code (3AC) | `lab4_icg.py` | `python lab4_icg.py valid.txt` | Linear Three-Address Code with temporaries (`t1`, `t2`) and 23-row Quadruples Table. |

---

## 2. Step-by-Step Lab Execution & Verification Guide

### 🧪 LAB 1: Lexical Analysis

#### How to Run:
```bash
python lab1_lexer.py valid.txt
python lab1_lexer.py lexical_error.txt
```

#### Results:
- **`valid.txt` Output:**
  ```text
  ==========================================================================
                    QUANTUMFLOW LEXICAL ANALYZER - LAB 1                    
  ==========================================================================
  #     Token Type        Lexeme                Line    Column  
  --------------------------------------------------------------------------
  1     INT               int                   1       1       
  2     ID                a                     1       5       
  3     OP_ASSIGN         :=                    1       7       
  4     NUM               5                     1       10      
  5     SEMICOLON         ;                     1       11      
  ...
  75    EOF               end of file           22      0       
  ==========================================================================
  Total Tokens Identified: 74 (+ 1 EOF marker)
  RESULT: Lexical Analysis Successful (No Lexical Errors)
  ==========================================================================
  ```
- **`lexical_error.txt` Output:**
  ```text
  Lexical Error at line 3, col 13: unrecognized character '@'

  RESULT: Lexical Analysis FAILED
  ```

---

### 🧪 LAB 2: Syntax Analysis (Parser)

#### How to Run:
```bash
python lab2_parser.py valid.txt
python lab2_parser.py syntax_error.txt
```

#### Results:
- **`valid.txt` Output:**
  ```text
  Parse Tree
  ----------
  Declaration: int a
    Num: 5
  Declaration: int b
    Num: 10
  Declaration: int sum
  Declaration: pulse big
    Bool: false
  Declaration: wave msg
    Str: "done"
  Assignment: sum
    Operator: .+.
      Id: a
      Operator: .*.
        Id: b
        Num: 2
  If
    Condition
      Operator: >>>
        Id: sum
        Num: 20
    Then
      Assignment: big
        Bool: true
    Else
      Assignment: big
        Bool: false
  While
    Condition
      Operator: <<<
        Id: a
        Id: b
    Body
      Assignment: a
        Operator: .+.
          Id: a
          Num: 1
  Print
    Id: sum
  Print
    Id: msg

  RESULT: Syntax is correct
  ```
- **`syntax_error.txt` Output:**
  ```text
  Syntax Error at line 3: expected ';' but found 'a'

  RESULT: Syntax is NOT correct
  ```

---

### 🧪 LAB 3: Semantic Analysis

#### How to Run:
```bash
python lab3_semantic.py valid.txt
python lab3_semantic.py semantic_error.txt
```

#### Results:
- **`valid.txt` Output:**
  ```text
  Symbol Table
  ------------
  Name      Type      Declared at line
  a         int       1
  b         int       2
  sum       int       3
  big       pulse     4
  msg       wave      5

  RESULT: No semantic errors
  ```
- **`semantic_error.txt` Output:**
  ```text
  Symbol Table
  ------------
  Name      Type      Declared at line
  a         int       1
  name      wave      3
  ok        pulse     4

  Semantic Error at line 2: variable 'a' is already declared at line 1
  Semantic Error at line 4: cannot store int value in pulse variable 'ok'
  Semantic Error at line 5: variable 'b' is not declared
  Semantic Error at line 6: operator '.+.' needs int operands but got int and wave
  Semantic Error at line 7: condition must be pulse but it is int

  RESULT: 5 semantic error(s) found
  ```

---

### 🧪 LAB 4: Intermediate Code Generation (3AC)

#### How to Run:
```bash
python lab4_icg.py valid.txt
python lab4_icg.py semantic_error.txt
```

#### Results:
- **`valid.txt` Output:**
  ```text
  Three-Address Code
  ------------------
      a = 5
      b = 10
      big = false
      msg = "done"
      t1 = b .*. 2
      t2 = a .+. t1
      sum = t2
      t3 = sum >>> 20
      ifFalse t3 goto L1
      big = true
      goto L2
  L1:
      big = false
  L2:
  L3:
      t4 = a <<< b
      ifFalse t4 goto L4
      t5 = a .+. 1
      a = t5
      goto L3
  L4:
      print sum
      print msg

  Quadruples
  ----------
  #   op        arg1      arg2      result
  0   =         5                   a
  1   =         10                  b
  2   =         false               big
  3   =         "done"              msg
  4   .*.       b         2         t1
  5   .+.       a         t1        t2
  6   =         t2                  sum
  7   >>>       sum       20        t3
  8   ifFalse   t3                  L1
  9   =         true                big
  10  goto                          L2
  11  label                         L1
  12  =         false               big
  13  label                         L2
  14  label                         L3
  15  <<<       a         b         t4
  16  ifFalse   t4                  L4
  17  .+.       a         1         t5
  18  =         t5                  a
  19  goto                          L3
  20  label                         L4
  21  print     sum                 
  22  print     msg                 
  ```
- **`semantic_error.txt` Output:**
  ```text
  Semantic Error at line 2: variable 'a' is already declared at line 1
  Semantic Error at line 4: cannot store int value in pulse variable 'ok'
  Semantic Error at line 5: variable 'b' is not declared
  Semantic Error at line 6: operator '.+.' needs int operands but got int and wave
  Semantic Error at line 7: condition must be pulse but it is int

  RESULT: Code not generated because of semantic errors
  ```

---

## 3. How to Submit

1. **Submit the `.docx` report directly:**
   - Open and print or submit: **`d:\CC Project\QuantumFlow_Compiler_Labs_Report.docx`**
2. **Submit Source Code & Test Files:**
   - Python code: `lab1_lexer.py`, `lab2_parser.py`, `lab3_semantic.py`, `lab4_icg.py`
   - Test files: `valid.txt`, `lexical_error.txt`, `syntax_error.txt`, `semantic_error.txt`
3. **Presentation / Viva:**
   - Both the command-line programs and the web app (`app.py`) can be demonstrated to your instructor.
