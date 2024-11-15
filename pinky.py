import sys
from utils import *
from tokens import *
from lexer import *
from parser import *
from interpreter import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 pinky.py <filename>')

    filename = sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        print(f"{Colors.OKBLUE}------------------Lexer------------------{Colors.ENDC}")
        tokens = Lexer(source).tokenize()
        for token in tokens:
            print(token)

        print(f"{Colors.OKBLUE}------------------Parser------------------{Colors.ENDC}")
        program = Parser(tokens).parse()
        pretty_print_stmts(program)

        print(f"{Colors.OKBLUE}------------------Interpreter------------------{Colors.ENDC}")
        interpreter = Interpreter()
        interpreter.interpret_program(program)

