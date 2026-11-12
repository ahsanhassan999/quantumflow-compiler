from lexer import tokenize
from parser import parse_code
from semantic import SemanticAnalyzer
from icg import CodeGenerator
from evaluator import Evaluator

code = '''
module module_check_sign():
    initiate
    x := 15
    when x >>> 0
        initiate
        show("positive")
        end
    otherwise
        initiate
        show("non-positive")
        end
    yield x
    end
'''

tokens = tokenize(code)
print(f"Token count: {len(tokens)}")

ast = parse_code(tokens)
print("AST parsed successfully!")

analyzer = SemanticAnalyzer()
sem = analyzer.analyze(ast)
print("Semantic check:", sem)

icg = CodeGenerator()
code_3ac = icg.generate(ast)
print("3AC instructions:")
for i in code_3ac:
    print(" ", str(i))

evaluator = Evaluator()
result = evaluator.run(ast)
print("Runtime result:", result)

