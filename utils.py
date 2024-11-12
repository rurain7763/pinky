from model import *

def pretty_print_ast(ast, indent = 0):
    indent_str = '-' * indent 
    if isinstance(ast, Integer):
        print(f'{indent_str}Integer[{ast.value}]')
    elif isinstance(ast, Float):
        print(f'{indent_str}Float[{ast.value}]')
    else:
        if isinstance(ast, BinOp):
            print(f'{indent_str}BinOp({ast.op.lexeme!r}')
            pretty_print_ast(ast.left, indent + 1)
            pretty_print_ast(ast.right, indent + 1)
        elif isinstance(ast, UnOp):
            print(f'{indent_str}UnOp({ast.op.lexeme!r}')
            pretty_print_ast(ast.operand, indent + 1)
        elif isinstance(ast, Grouping):
            print(f'{indent_str}Grouping(')
            pretty_print_ast(ast.value, indent + 1)

        print(f'{indent_str})')