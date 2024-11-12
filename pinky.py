import sys
from tokens import *
from lexer import *
from parser import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 pinky.py <filename>')

    filename =sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        print("Lexer:")
        tokens = Lexer(source).tokenize()
        for token in tokens:
            print(token)

        print("Paser:")
        ast = Paser(tokens).parse()
        print(ast)

