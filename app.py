"""
Flask Web Application for QuantumFlow Compiler Construction Project.
Features:
- Dedicated Grammar Definition Section (Interactive CFG & Vocabulary)
- Independent Execution for each Compiler Engine:
    1. Lexical Engine (/engine/lexical)
    2. Syntax Engine (/engine/syntax)
    3. Semantic Engine (/engine/semantic)
    4. ICG Engine (/engine/icg)
    5. Full Pipeline Runner (/engine/all)
- User Authentication (Login / Register / Session management)
- Persistent Audit Logging (Tracks who executed what engine with timestamps & outcomes)
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from lexer import tokenize
from parser import parse_code
from semantic import SemanticAnalyzer
from icg import CodeGenerator
from evaluator import Evaluator
import database

app = Flask(__name__)
app.secret_key = "quantumflow-secret-key-cc-project-2026"

# Initialize DB on startup
database.init_db()

SAMPLE_PROGRAMS = {
    "check_sign": {
        "title": "1. Lab Snippet (When / Otherwise)",
        "code": """# Module to check if a number is positive
module module_check_sign():
    initiate
    x := 15
    when x >>> 0
        initiate
        show("Value is positive!")
        end
    otherwise
        initiate
        show("Value is non-positive!")
        end
    yield x
    end"""
    },
    "cycle_loop": {
        "title": "2. Iterative Cycle Loop (Counter & Sum)",
        "code": """# Counting with cycle loop and custom addition
initiate
count := 1
sum := 0
cycle count <<< 6
    initiate
    show("Current count is:")
    show(count)
    sum := sum .+. count
    count := count .+. 1
    end
show("Final Total Sum:")
show(sum)
yield sum
end"""
    },
    "logical_arithmetic": {
        "title": "3. Custom Operators (.+., .-., &&&, ==?)",
        "code": """# Testing custom operators
initiate
a := 20
b := 10
c := a .-. b
show("Result of a .-. b:")
show(c)

when (c ==? 10) &&& (a >>> b)
    initiate
    show("Both conditions matched successfully!")
    end
otherwise
    initiate
    show("Condition failed.")
    end
yield c
end"""
    },
    "syntax_error_demo": {
        "title": "4. Syntax Error Test (Missing Right Operand)",
        "code": """# Syntax Error: Incomplete expression
initiate
a := 10
b := a .+. 
show(b)
end"""
    },
    "semantic_error_demo": {
        "title": "5. Semantic Error Test (Undeclared Var)",
        "code": """# Semantic Error: Variable used before declaration
initiate
known_var := 100
result := known_var .+. undeclared_var
show(result)
end"""
    }
}

GROUP_MEMBERS = [
    {"name": "Syed Ahsan Hassan Rizvi", "roll": "EB-24210006096", "role": "Group Leader"},
    {"name": "Sami Ur Rehman", "roll": "EB-24210006086", "role": "Group Member"},
    {"name": "M. Behroz Abid", "roll": "EB-24210006001", "role": "Group Member"}
]

def current_user():
    return session.get("user", {"username": "Guest", "role": "Visitor", "full_name": "Guest Visitor"})

# ----------------- Auth Routes -----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    
    user = database.verify_user(username, password)
    if user:
        session["user"] = {
            "username": user["username"],
            "full_name": user["full_name"],
            "roll_number": user["roll_number"],
            "role": user["role"]
        }
        database.log_action(user["username"], "USER_LOGIN", "SUCCESS", f"User logged in from web interface", "")
        return jsonify({"success": True, "user": session["user"]})
    else:
        return jsonify({"success": False, "error": "Invalid username or password."}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    full_name = data.get("full_name", "")
    roll_number = data.get("roll_number", "")
    
    if not username or not password or not full_name:
        return jsonify({"success": False, "error": "All fields are required."}), 400
        
    ok, msg = database.register_user(username, password, full_name, roll_number)
    if ok:
        database.log_action(username, "USER_REGISTER", "SUCCESS", f"Registered account for {full_name}", "")
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/logout", methods=["POST"])
def logout():
    user = current_user()
    database.log_action(user["username"], "USER_LOGOUT", "SUCCESS", "Logged out", "")
    session.pop("user", None)
    return jsonify({"success": True})

@app.route("/api/user")
def get_user():
    return jsonify({"user": current_user()})

# ----------------- Logs Route -----------------
@app.route("/api/logs")
def get_logs():
    logs = database.get_recent_logs(60)
    return jsonify({"logs": logs})

@app.route("/api/logs/clear", methods=["POST"])
def clear_logs():
    user = current_user()
    database.clear_all_logs()
    database.log_action(user["username"], "LOGS_CLEARED", "SUCCESS", "Audit logs cleared by user", "")
    return jsonify({"success": True})

# ----------------- Main View -----------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        samples=SAMPLE_PROGRAMS,
        group=GROUP_MEMBERS,
        user=current_user()
    )

# ----------------- Independent Engines -----------------

# Engine 1: Independent Lexical Analyzer
@app.route("/engine/lexical", methods=["POST"])
def run_lexical():
    user = current_user()["username"]
    code = (request.get_json() or {}).get("code", "")
    try:
        tokens = tokenize(code)
        tok_list = [
            {"type": t.type, "value": t.value, "line": t.line, "column": t.column}
            for t in tokens if t.type != 'EOF'
        ]
        database.log_action(user, "ENGINE_LEXICAL", "SUCCESS", f"Generated {len(tok_list)} tokens", code)
        return jsonify({"success": True, "tokens": tok_list, "token_count": len(tok_list)})
    except Exception as e:
        err_msg = str(e)
        database.log_action(user, "ENGINE_LEXICAL", "ERROR", err_msg, code)
        return jsonify({"success": False, "error": err_msg})

# Engine 2: Independent Syntax Analyzer (Parser)
@app.route("/engine/syntax", methods=["POST"])
def run_syntax():
    user = current_user()["username"]
    code = (request.get_json() or {}).get("code", "")
    try:
        tokens = tokenize(code)
        ast = parse_code(tokens)
        database.log_action(user, "ENGINE_SYNTAX", "SUCCESS", "AST generated successfully", code)
        return jsonify({"success": True, "ast": ast.to_dict()})
    except Exception as e:
        err_msg = str(e)
        database.log_action(user, "ENGINE_SYNTAX", "ERROR", err_msg, code)
        return jsonify({"success": False, "error": err_msg})

# Engine 3: Independent Semantic Analyzer
@app.route("/engine/semantic", methods=["POST"])
def run_semantic():
    user = current_user()["username"]
    code = (request.get_json() or {}).get("code", "")
    try:
        tokens = tokenize(code)
        ast = parse_code(tokens)
        analyzer = SemanticAnalyzer()
        res = analyzer.analyze(ast)
        if res["success"]:
            database.log_action(user, "ENGINE_SEMANTIC", "SUCCESS", f"Verified {len(res['symbol_table'])} symbols with 0 errors", code)
            return jsonify({"success": True, "symbol_table": res["symbol_table"]})
        else:
            err_msg = "\n".join(res["errors"])
            database.log_action(user, "ENGINE_SEMANTIC", "ERROR", f"{len(res['errors'])} semantic error(s)", code)
            return jsonify({"success": False, "symbol_table": res["symbol_table"], "error": err_msg, "errors": res["errors"]})
    except Exception as e:
        err_msg = str(e)
        database.log_action(user, "ENGINE_SEMANTIC", "ERROR", err_msg, code)
        return jsonify({"success": False, "error": err_msg})

# Engine 4: Independent Intermediate Code Generator (ICG)
@app.route("/engine/icg", methods=["POST"])
def run_icg():
    user = current_user()["username"]
    code = (request.get_json() or {}).get("code", "")
    try:
        tokens = tokenize(code)
        ast = parse_code(tokens)
        analyzer = SemanticAnalyzer()
        sem_res = analyzer.analyze(ast)
        if not sem_res["success"]:
            err_msg = "Cannot generate 3AC due to semantic errors:\n" + "\n".join(sem_res["errors"])
            database.log_action(user, "ENGINE_ICG", "ERROR", "Blocked by semantic errors", code)
            return jsonify({"success": False, "error": err_msg})
        
        icg = CodeGenerator()
        instructions = icg.generate(ast)
        instr_list = [i.to_dict() for i in instructions]
        database.log_action(user, "ENGINE_ICG", "SUCCESS", f"Generated {len(instr_list)} 3AC instructions", code)
        return jsonify({"success": True, "instructions": instr_list})
    except Exception as e:
        err_msg = str(e)
        database.log_action(user, "ENGINE_ICG", "ERROR", err_msg, code)
        return jsonify({"success": False, "error": err_msg})

# Engine 5: Full Compilation & Execution Pipeline
@app.route("/compile", methods=["POST"])
def run_full_pipeline():
    user = current_user()["username"]
    code = (request.get_json() or {}).get("code", "")
    
    response = {
        "success": True,
        "current_stage": "",
        "lexical": {"tokens": [], "error": None},
        "syntax": {"ast": None, "error": None},
        "semantic": {"symbol_table": [], "errors": [], "error": None},
        "icg": {"instructions": [], "error": None},
        "runtime": {"output": "", "yield_value": None, "variables": {}, "error": None}
    }

    # 1. Lexical
    try:
        tokens = tokenize(code)
        response["lexical"]["tokens"] = [
            {"type": t.type, "value": t.value, "line": t.line, "column": t.column}
            for t in tokens if t.type != 'EOF'
        ]
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Lexical Analysis"
        response["lexical"]["error"] = str(e)
        database.log_action(user, "FULL_PIPELINE", "ERROR", f"Failed at Lexical: {e}", code)
        return jsonify(response)

    # 2. Syntax
    try:
        ast = parse_code(tokens)
        response["syntax"]["ast"] = ast.to_dict()
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Syntax Analysis"
        response["syntax"]["error"] = str(e)
        database.log_action(user, "FULL_PIPELINE", "ERROR", f"Failed at Syntax: {e}", code)
        return jsonify(response)

    # 3. Semantic
    try:
        analyzer = SemanticAnalyzer()
        sem = analyzer.analyze(ast)
        response["semantic"]["symbol_table"] = sem["symbol_table"]
        response["semantic"]["errors"] = sem["errors"]
        if not sem["success"]:
            response["success"] = False
            response["current_stage"] = "Semantic Analysis"
            response["semantic"]["error"] = "\n".join(sem["errors"])
            database.log_action(user, "FULL_PIPELINE", "ERROR", f"Failed at Semantic: {len(sem['errors'])} errors", code)
            return jsonify(response)
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Semantic Analysis"
        response["semantic"]["error"] = str(e)
        database.log_action(user, "FULL_PIPELINE", "ERROR", f"Failed at Semantic: {e}", code)
        return jsonify(response)

    # 4. ICG
    try:
        icg = CodeGenerator()
        instrs = icg.generate(ast)
        response["icg"]["instructions"] = [i.to_dict() for i in instrs]
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Intermediate Code Generation"
        response["icg"]["error"] = str(e)
        database.log_action(user, "FULL_PIPELINE", "ERROR", f"Failed at ICG: {e}", code)
        return jsonify(response)

    # 5. Runtime Evaluator
    try:
        evaluator = Evaluator()
        run_res = evaluator.run(ast)
        if not run_res["success"]:
            response["success"] = False
            response["current_stage"] = "Runtime Execution"
            response["runtime"]["error"] = run_res.get("error")
            database.log_action(user, "FULL_PIPELINE", "ERROR", f"Runtime Error: {run_res.get('error')}", code)
        else:
            database.log_action(user, "FULL_PIPELINE", "SUCCESS", "All 5 stages completed successfully", code)
            
        response["runtime"]["output"] = run_res.get("output", "")
        response["runtime"]["yield_value"] = run_res.get("yield_value")
        response["runtime"]["variables"] = run_res.get("variables", {})
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Runtime Execution"
        response["runtime"]["error"] = str(e)
        database.log_action(user, "FULL_PIPELINE", "ERROR", f"Runtime Crash: {e}", code)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
