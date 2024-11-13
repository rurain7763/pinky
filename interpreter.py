from model import *
from tokens import *
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER'
TYPE_BOOL   = 'TYPE_BOOL'
TYPE_STRING = 'TYPE_STRING'

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, ast):
        if isinstance(ast, Integer):
            return (TYPE_NUMBER, float(ast.value))
        elif isinstance(ast, Float):
            return (TYPE_NUMBER, ast.value)
        elif isinstance(ast, Bool):
            return (TYPE_BOOL, ast.value)
        elif isinstance(ast, String):
            return (TYPE_STRING, ast.value)
        elif isinstance(ast, Grouping):
            return self.interpret(ast.value)
        elif isinstance(ast, BinOp):
            left_type, left_value = self.interpret(ast.left)
            right_type, right_value = self.interpret(ast.right)
            if ast.op.token_type == TOK_PLUS: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value + right_value)
                elif left_type == TYPE_STRING or right_type == TYPE_STRING:
                    return (TYPE_STRING, str(left_value) + str(right_value))
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_MINUS: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value - right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_STAR: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value * right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_SLASH: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value / right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_MOD:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value % right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_CARET:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value ** right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_LT:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value < right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_GT:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value > right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_LE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value <= right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_GE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value >= right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_EQEQ:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING) or (left_type == TYPE_BOOL and right_type == TYPE_BOOL):
                    return (TYPE_BOOL, left_value == right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_NE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING) or (left_type == TYPE_BOOL and right_type == TYPE_BOOL):
                    return (TYPE_BOOL, left_value != right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
        elif isinstance(ast, UnOp):
            type, val = self.interpret(ast.operand)
            if ast.op.token_type == TOK_PLUS: 
                if type == TYPE_NUMBER:
                    return (TYPE_NUMBER, +val)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} at {type}', ast.line)
            elif ast.op.token_type == TOK_MINUS: 
                if type == TYPE_NUMBER:
                    return (TYPE_NUMBER, -val)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} at {type}', ast.line)
            elif ast.op.token_type == TOK_NOT: 
                if type == TYPE_BOOL:
                    return (TYPE_BOOL, not val)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} at {type}', ast.line)
        elif isinstance(ast, LogicalOp):
            left_type, left_value = self.interpret(ast.left)
            right_type, right_value = self.interpret(ast.right)
            if ast.op.token_type == TOK_OR:
                if left_type == TYPE_BOOL and right_type == TYPE_BOOL:
                    return (TYPE_BOOL, left_value or right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
            elif ast.op.token_type == TOK_AND:
                if left_type == TYPE_BOOL and right_type == TYPE_BOOL:
                    return (TYPE_BOOL, left_value and right_value)
                else:
                    runtime_error(f'Unsupported operator {ast.op.lexeme!r} between {left_type} and {right_type}', ast.line)
        