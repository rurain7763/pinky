from model import *

def print_stmt(stmt, indent = 0):
    if isinstance(stmt, PrintStmt):
        if stmt.end == '': print(f'{' ' * indent}PrintStmt(')
        elif stmt.end == '\n': print(f'{' ' * indent}PrintlnStmt(')
        pretty_print_ast(stmt.value, indent + 1)
    elif isinstance(stmt, IfStmt):
        print(f'{' ' * indent}IfStmt(')
        pretty_print_ast(stmt.condition, indent + 1)
        pretty_print_stmts(stmt.then_stmts, indent + 1, prefix='then:')
        if stmt.else_stmts:
            pretty_print_stmts(stmt.else_stmts, indent + 1, prefix='else:')
    elif isinstance(stmt, Assignment):
        print(f'{' ' * indent}Assignment(')
        pretty_print_ast(stmt.left, indent + 1)
        pretty_print_ast(stmt.right, indent + 1)
    elif isinstance(stmt, WhileStmt):
        print(f'{' ' * indent}WhileStmt(')
        pretty_print_ast(stmt.condition, indent + 1)
        pretty_print_stmts(stmt.do_stmts, indent + 1, prefix='do:')
    elif isinstance(stmt, ForStmt):
        print(f'{' ' * indent}ForStmt(')
        print_stmt(stmt.assignment, indent + 1)
        pretty_print_ast(stmt.condition_val, indent + 1, prefix='cond:')
        pretty_print_ast(stmt.step_val, indent + 1, prefix='inc:')
        pretty_print_stmts(stmt.do_stmts, indent + 1, prefix='do:')
    elif isinstance(stmt, FuncDecl):
        print(f'{' ' * indent}FuncDecl(')
        pretty_print_ast(stmt.name, indent + 1, prefix='name:')
        for param in stmt.params:
            print_stmt(param, indent + 1)
        pretty_print_stmts(stmt.body_stmts, indent + 1, prefix='body:')
    elif isinstance(stmt, Param):
        print(f'{' ' * indent}Param(')
        pretty_print_ast(stmt.name, indent + 1)
    elif isinstance(stmt, FuncCallStmt):
        print(f'{' ' * indent}FuncCallStmt(')
        pretty_print_ast(stmt.func_call, indent + 1)
            
    print(f'{' ' * indent})')

def pretty_print_stmts(stmts, indent = 0, prefix = ''):
    backup_indent = indent
    print(f'{' ' * indent}{prefix}Stmts(')

    indent = indent + 1
    for stmt in stmts.stmts:
        print_stmt(stmt, indent)

    indent = backup_indent
    print(f'{' ' * indent})')

def pretty_print_ast(ast, indent = 0, prefix = ''):
    indent_str = ' ' * indent 
    if isinstance(ast, Integer):
        print(f'{indent_str}{prefix}Integer[{ast.value}]')
    elif isinstance(ast, Float):
        print(f'{indent_str}{prefix}Float[{ast.value}]')
    elif isinstance(ast, Bool):
        print(f'{indent_str}Bool[{ast.value}]')
    elif isinstance(ast, String):
        print(f'{indent_str}String[{ast.value}]')
    elif isinstance(ast, Identifier):
        print(f'{indent_str}Identifier[{ast.name}]')
    else:
        if isinstance(ast, BinOp):
            print(f'{indent_str}BinOp({ast.op.lexeme!r}')
            pretty_print_ast(ast.left, indent + 1)
            pretty_print_ast(ast.right, indent + 1)
        elif isinstance(ast, UnOp):
            print(f'{indent_str}UnOp({ast.op.lexeme!r}')
            pretty_print_ast(ast.operand, indent + 1)
        elif isinstance(ast, LogicalOp):
            print(f'{indent_str}LogicalOp({ast.op.lexeme!r}')
            pretty_print_ast(ast.left, indent + 1)
            pretty_print_ast(ast.right, indent + 1)
        elif isinstance(ast, Grouping):
            print(f'{indent_str}Grouping(')
            pretty_print_ast(ast.value, indent + 1)
        elif isinstance(ast, FuncCall):
            print(f'{indent_str}FuncCall(')
            pretty_print_ast(ast.name, indent + 1)
            for arg in ast.args:
                pretty_print_ast(arg, indent + 1)

        print(f'{indent_str})')

def stringify(value):
    if isinstance(value, bool) and value is True:
        return "true"
    elif isinstance(value, bool) and value is False:
        return "false"
    elif isinstance(value, float) and value.is_integer():
        return str(int(value))
    else:
        return str(value)

def parse_error(msg, lineno):
    print(f'{Colors.FAIL}[Line {lineno}] {msg}{Colors.ENDC}')
    import sys
    sys.exit(1)

def lexeing_error(msg, lineno):
    print(f'{Colors.FAIL}[Line {lineno}] {msg}{Colors.ENDC}')
    import sys
    sys.exit(1)

def runtime_error(msg, lineno):
    print(f'{Colors.FAIL}[Line {lineno}] {msg}{Colors.ENDC}')
    import sys
    sys.exit(1)
    
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'