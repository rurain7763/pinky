import sys
from utils import *
from tokens import *
from lexer import *
from parser import *
from interpreter import *

DEBUG = False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 pinky.py <filename>')

    filename = sys.argv[1]

    with open(filename) as file:
        source = file.read()

        tokens = Lexer(source).tokenize()

        if DEBUG:
            print(f"{Colors.OKBLUE}------------------Lexer------------------{Colors.ENDC}")
            for token in tokens:
                print(token)

        program = Parser(tokens).parse()

        if DEBUG:
            print(f"{Colors.OKBLUE}------------------Parser------------------{Colors.ENDC}")
            pretty_print_stmts(program)
        
        if DEBUG:
            print(f"{Colors.OKBLUE}------------------Interpreter------------------{Colors.ENDC}")
            
        interpreter = Interpreter()
        interpreter.interpret_program(program)

