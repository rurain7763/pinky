import sys
from utils import *
from tokens import *
from lexer import *
from parser import *
from interpreter import *
from compiler import *
from vm import *

DEBUG = True

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

        ast = Parser(tokens).parse()

        if DEBUG:
            print(f"{Colors.OKBLUE}------------------Parser------------------{Colors.ENDC}")
            pretty_print_stmts(ast)
        
        # if DEBUG:
        #    print(f"{Colors.OKBLUE}------------------Interpreter------------------{Colors.ENDC}")
            
        # interpreter = Interpreter()
        # interpreter.interpret_program(ast)

        if DEBUG:
            print(f"{Colors.OKBLUE}------------------Compiler------------------{Colors.ENDC}")

        compiler = Compiler()
        instructions = compiler.generate_code(ast)
        pretty_print_instructions(instructions)

        if DEBUG:
            print(f"{Colors.OKBLUE}------------------VM------------------{Colors.ENDC}")

        vm = VM()
        vm.run(instructions)

