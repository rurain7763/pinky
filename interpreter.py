from model import *
from tokens import *
from utils import *
import codecs

TYPE_NUMBER = 'TYPE_NUMBER'
TYPE_BOOL   = 'TYPE_BOOL'
TYPE_STRING = 'TYPE_STRING'

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, node):
        if isinstance(node, Integer):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, Float):
            return (TYPE_NUMBER, node.value)
        elif isinstance(node, Bool):
            return (TYPE_BOOL, node.value)
        elif isinstance(node, String):
            return (TYPE_STRING, node.value)
        elif isinstance(node, Grouping):
            return self.interpret(node.value)
        elif isinstance(node, BinOp):
            left_type, left_value = self.interpret(node.left)
            right_type, right_value = self.interpret(node.right)
            if node.op.token_type == TOK_PLUS: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value + right_value)
                elif left_type == TYPE_STRING or right_type == TYPE_STRING:
                    return (TYPE_STRING, str(left_value) + str(right_value))
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_MINUS: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value - right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_STAR: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value * right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_SLASH: 
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    if(right_value == 0):
                        runtime_error(f'Error: Division by zero', node.line)
                    else:
                        return (TYPE_NUMBER, left_value / right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_MOD:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value % right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_CARET:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_value ** right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_LT:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value < right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_GT:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value > right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_LE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value <= right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_GE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING):
                    return (TYPE_BOOL, left_value >= right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_EQEQ:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING) or (left_type == TYPE_BOOL and right_type == TYPE_BOOL):
                    return (TYPE_BOOL, left_value == right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
            elif node.op.token_type == TOK_NE:
                if (left_type == TYPE_NUMBER and right_type == TYPE_NUMBER) or (left_type == TYPE_STRING and right_type == TYPE_STRING) or (left_type == TYPE_BOOL and right_type == TYPE_BOOL):
                    return (TYPE_BOOL, left_value != right_value)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {left_type} and {right_type}', node.line)
        elif isinstance(node, UnOp):
            type, val = self.interpret(node.operand)
            if node.op.token_type == TOK_PLUS: 
                if type == TYPE_NUMBER:
                    return (TYPE_NUMBER, +val)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} at {type}', node.line)
            elif node.op.token_type == TOK_MINUS: 
                if type == TYPE_NUMBER:
                    return (TYPE_NUMBER, -val)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} at {type}', node.line)
            elif node.op.token_type == TOK_NOT: 
                if type == TYPE_BOOL:
                    return (TYPE_BOOL, not val)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} at {type}', node.line)
        elif isinstance(node, LogicalOp):
            left_type, left_value = self.interpret(node.left)
            if (node.op.token_type == TOK_AND and left_value) or (node.op.token_type == TOK_OR and not left_value):
                return self.interpret(node.right)
            else:
                return (left_type, left_value)
        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.interpret(stmt)
        elif isinstance(node, PrintStmt):
            type, value = self.interpret(node.value)
            print(codecs.escape_decode(bytes(str(value), 'utf-8'))[0].decode('utf-8'), end = node.end)
