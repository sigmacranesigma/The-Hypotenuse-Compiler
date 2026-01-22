import sys
from lexer import get_tokens
import parser as parse
from codegen import PythonCodeGen

def main():
    if len(sys.argv) < 2:
        print("usage: python main.py <source_file>")
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        content = file.read()

    # lexing stuffs
    tokens = get_tokens(content)
    tokens.append(('EOF', 'EOF', len(content)))

    # parsing stuffs
    p = parse.Parser(tokens)
    ast = p.parse_program()

    # codegen
    cg = PythonCodeGen()
    python_code = cg.generate(ast)

    # codegen output
    print("code generated (python)")
    print(python_code)

if __name__ == "__main__":
    main()
