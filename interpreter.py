from model import *
from tokens import *

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, ast):
        if isinstance(ast, Integer):
            return float(ast.value)
        elif isinstance(ast, Float):
            return float(ast.value)
        elif isinstance(ast, Grouping):
            return self.interpret(ast.value)
        elif isinstance(ast, BinOp):
            left = self.interpret(ast.left)
            right = self.interpret(ast.right)
            if ast.op.token_type == TOK_PLUS: return left + right
            elif ast.op.token_type == TOK_MINUS: return left - right
            elif ast.op.token_type == TOK_STAR: return left * right
            elif ast.op.token_type == TOK_SLASH: return left / right
        elif isinstance(ast, UnOp):
            val = self.interpret(ast.operand)
            if ast.op.token_type == TOK_PLUS: return +val
            elif ast.op.token_type == TOK_MINUS: return -val
            elif ast.op.token_type == TOK_NOT: return not val