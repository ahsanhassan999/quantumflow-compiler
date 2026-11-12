# QuantumFlow Compiler Pipeline (Web Application)

**Course:** Compiler Construction (CS)  
**Project Title:** Interactive 5-Stage Web-Based Compiler for *QuantumFlow*

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
| Equality check | `==?` | `x ==? y` |
| Not equal | `!=?` | `x !=? y` |
| Greater than | `>>>` | `x >>> y` |
| Less than | `<<<` | `x <<< y` |
| Logical AND | `&&&` | `x &&& y` |
| Logical OR | `\|\|\|` | `x \|\|\| y` |

---

## 🏗️ Compiler Architecture & 5 Stages

This web application allows the user or instructor to write or select QuantumFlow code and inspect all five classical compilation stages:

1. **Lexical Analysis (`lexer.py`)**:
   - Tokenizes source code into `(TokenType, Lexeme, Line, Column)`.
   - Recognizes multi-character custom operators and keywords.
   - Detects unrecognized characters with line/col reporting.

2. **Syntax Analysis (`parser.py`)**:
   - Uses a **Recursive Descent Parser** to check Grammar (CFG) compliance.
   - Constructs and renders an **Abstract Syntax Tree (AST)**.

3. **Semantic Analysis (`semantic.py`)**:
   - Scope resolution and variable declaration checking.
   - Generates a formatted **Symbol Table** (Symbol, Type, Scope, Line, Value).
   - Detects use of uninitialized/undeclared variables and type mismatches.

4. **Intermediate Code Generation (`icg.py`)**:
   - Generates machine-independent **Three-Address Code (3AC)**.
   - Outputs both linear 3AC representation and a **Quadruples Table** `(Op, Arg1, Arg2, Result)`.

5. **Code Execution & Evaluation (`evaluator.py`)**:
   - Executes the program instructions.
   - Displays real-time standard output from `show()` and captures `yield` values.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-link>
   cd "CC Project"
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Start the web application:**
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🌐 Free Deployment to Render (or Railway / PythonAnywhere)

1. Push this project to your GitHub repository.
2. Go to [Render.com](https://render.com) and log in with GitHub.
3. Click **New +** -> **Web Service**.
4. Select your `CC Project` repository.
5. Set:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click **Deploy Web Service**. You will receive a public live URL to share with your instructor!

