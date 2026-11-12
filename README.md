# QuantumFlow Compiler Pipeline (Web Application & Lab Suite)

**Course:** Compiler Construction (CS)  
**Project Title:** Interactive 5-Stage Web-Based Compiler for *QuantumFlow*  
**Live Web Application:** 🌐 [https://quantumflow-compiler.onrender.com/](https://quantumflow-compiler.onrender.com/)

---

## 👥 Group Members
1. **Syed Ahsan Hassan Rizvi** (EB-24210006096) — **Group Leader**
2. **Sami Ur Rehman** (EB-24210006086) — **Group Member**
3. **M. Behroz Abid** (EB-24210006001) — **Group Member**

---

## 🌟 Language Specification: *QuantumFlow*

QuantumFlow is a custom programming language designed around the concept of state transitions and explicit control combinators.

### Custom Keywords
| Standard Keyword | QuantumFlow Keyword | Description |
|------------------|---------------------|-------------|
| `int`            | `int`               | Integer primitive data type |
| `bool`           | `pulse`             | Boolean primitive data type (`true` / `false`) |
| `string`         | `wave`              | String sequence data type |
| `begin / start`  | `initiate`          | Marks the start of a block / entry point |
| `if`             | `when`              | Conditional branch |
| `else`           | `otherwise`         | Alternate branch of a condition |
| `function`       | `module`            | Reusable procedure or module declaration |
| `return`         | `yield`             | Returns an evaluation result |
| `while / loop`   | `cycle`             | Loop iteration |
| `print`          | `show`              | Built-in console print |
| `end`            | `end`               | Explicit block closure |

### Custom Operators
| Operation | Custom Operator | Example |
|-----------|-----------------|---------|
| Assignment | `:=` | `x := 10` |
| Addition | `.+..` | `x .+. y` |
| Subtraction | `.-.` | `x .-. y` |
| Multiplication | `.*.` | `x .*. y` |
| Division | `./.` | `x ./. y` |
| Equality check | `==?` | `x ==? y` |
| Not equal | `!=?` | `x !=? y` |
| Greater than | `>>>` | `x >>> y` |
| Less than | `<<<` | `x <<< y` |
| Logical AND | `&&&` | `x &&& y` |
| Logical OR | `\|\|\|` | `x \|\|\| y` |

---

## 🏗️ Compiler Architecture & 4 Independent Engines

The web application allows the user or instructor to write or select QuantumFlow code and inspect all compilation stages either **individually** or as a **complete pipeline**:

1. **Section 1: Grammar Definition (CFG)**:
   - Visual cards showing custom keywords & operators.
   - Formal Context-Free Grammar (EBNF rules) for expression hierarchy, blocks, and statements.

2. **Section 2: Code Editor & 4 Independent Engines**:
   - **Lexical Analysis Engine (`/engine/lexical`)**: Deterministic token scanning (Type, Lexeme, Line, Col).
   - **Syntax Analysis Engine (`/engine/syntax`)**: Recursive Descent Parser building the Abstract Syntax Tree (AST).
   - **Semantic Analysis Engine (`/engine/semantic`)**: Scoped Symbol Table & type/declaration checker.
   - **Intermediate Code Engine (`/engine/icg`)**: Machine-independent Three-Address Code (3AC) and Quadruples Table `(Op, Arg1, Arg2, Result)`.
   - **Complete Pipeline Runner**: Runs all 4 engines and evaluates code in the Virtual Machine to display console output.

3. **User Authentication & Persistent Audit Logs**:
   - Role-based user login (`Group Leader`, `Group Member`, `Evaluator`).
   - SQLite audit logging tracking who triggered what engine with exact timestamps and code snippets.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahsanhassan999/quantumflow-compiler.git
   cd quantumflow-compiler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the web application:**
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🌐 Live Cloud Deployment

The application is deployed and accessible 24/7 at:  
👉 **[https://quantumflow-compiler.onrender.com/](https://quantumflow-compiler.onrender.com/)**
