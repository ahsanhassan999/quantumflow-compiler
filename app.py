"""
Flask Web Application for QuantumFlow Compiler Construction Project.
Group Members:
1. Syed Ahsan Hassan Rizvi (EB-24210006096) (Leader)
2. Sami Ur Rehman (EB-24210006086)
3. M. Behroz Abid (EB-24210006001)
"""

from flask import Flask, render_template, request, jsonify
from lexer import tokenize
from parser import parse_code
from semantic import SemanticAnalyzer
from icg import CodeGenerator
from evaluator import Evaluator

app = Flask(__name__)

# Pre-packaged sample QuantumFlow programs for sir to test easily
SAMPLE_PROGRAMS = {
    "check_sign": {
        "title": "1. Lab Snippet (Check Sign)",
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
        "title": "2. Iterative Cycle Loop (Factorial/Counter)",
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
        "title": "3. Complex Operators (.+., .-., &&&, ==?)",
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
    "semantic_error": {
        "title": "4. Semantic Error Test (Undeclared Var)",
        "code": """# Demonstrating Semantic Analysis Error Detection
initiate
known_var := 100
# 'unknown_var' has not been declared/assigned
result := known_var .+. unknown_var
show(result)
end"""
    }
}

@app.route("/")
def index():
    group_info = [
        {"name": "Syed Ahsan Hassan Rizvi", "roll": "EB-24210006096", "role": "Group Leader"},
        {"name": "Sami Ur Rehman", "roll": "EB-24210006086", "role": "Group Member"},
        {"name": "M. Behroz Abid", "roll": "EB-24210006001", "role": "Group Member"}
    ]
    return render_template("index.html", samples=SAMPLE_PROGRAMS, group=group_info)

@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.get_json() or {}
    source_code = data.get("code", "")

    response = {
        "success": True,
        "current_stage": "",
        "lexical": {"tokens": [], "error": None},
        "syntax": {"ast": None, "error": None},
        "semantic": {"symbol_table": [], "errors": [], "error": None},
        "icg": {"instructions": [], "error": None},
        "runtime": {"output": "", "yield_value": None, "variables": {}, "error": None}
    }

    # Stage 1: Lexical Analysis
    try:
        tokens = tokenize(source_code)
        response["lexical"]["tokens"] = [
            {"type": t.type, "value": t.value, "line": t.line, "column": t.column}
            for t in tokens if t.type != 'EOF'
        ]
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Lexical Analysis"
        response["lexical"]["error"] = str(e)
        return jsonify(response)

    # Stage 2: Syntax Analysis (Parser)
    try:
        ast = parse_code(tokens)
        response["syntax"]["ast"] = ast.to_dict()
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Syntax Analysis"
        response["syntax"]["error"] = str(e)
        return jsonify(response)

    # Stage 3: Semantic Analysis
    try:
        analyzer = SemanticAnalyzer()
        sem_res = analyzer.analyze(ast)
        response["semantic"]["symbol_table"] = sem_res["symbol_table"]
        response["semantic"]["errors"] = sem_res["errors"]
        if not sem_res["success"]:
            response["success"] = False
            response["current_stage"] = "Semantic Analysis"
            response["semantic"]["error"] = "\n".join(sem_res["errors"])
            return jsonify(response)
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Semantic Analysis"
        response["semantic"]["error"] = str(e)
        return jsonify(response)

    # Stage 4: Intermediate Code Generation (ICG)
    try:
        icg = CodeGenerator()
        instructions = icg.generate(ast)
        response["icg"]["instructions"] = [instr.to_dict() for instr in instructions]
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Intermediate Code Generation"
        response["icg"]["error"] = str(e)
        return jsonify(response)

    # Stage 5: Final Execution / Runtime Evaluator
    try:
        evaluator = Evaluator()
        eval_res = evaluator.run(ast)
        if not eval_res["success"]:
            response["success"] = False
            response["current_stage"] = "Runtime Execution"
            response["runtime"]["error"] = eval_res.get("error")
        response["runtime"]["output"] = eval_res.get("output", "")
        response["runtime"]["yield_value"] = eval_res.get("yield_value")
        response["runtime"]["variables"] = eval_res.get("variables", {})
    except Exception as e:
        response["success"] = False
        response["current_stage"] = "Runtime Execution"
        response["runtime"]["error"] = str(e)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

