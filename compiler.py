from model import *
from tokens import *
from utils import *
from state import *

TYPE_NUMBER = 'TYPE_NUMBER'
TYPE_BOOL   = 'TYPE_BOOL'
TYPE_STRING = 'TYPE_STRING'

class Compiler:
    def __init__(self):
        self.code = []

    def emit(self, instruction):
        self.code.append(instruction)

    def compile(self, node):
        if isinstance(node, Integer):
            value = (TYPE_NUMBER, float(node.value))
            self.emit(('PUSH', value))
        elif isinstance(node, Float):
            value = (TYPE_NUMBER, float(node.value))
            self.emit(('PUSH', value))
        elif isinstance(node, Bool):
            value = (TYPE_BOOL, node.value)
            self.emit(('PUSH', value))
        elif isinstance(node, String):
            value = (TYPE_STRING, stringify(node.value))
            self.emit(('PUSH', value))
        elif isinstance(node, Grouping):
            self.compile(node.value)
        elif isinstance(node, BinOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TOK_PLUS:
                self.emit(('ADD', None))
            elif node.op.token_type == TOK_MINUS:
                self.emit(('SUB', None))
            elif node.op.token_type == TOK_STAR:
                self.emit(('MUL', None))
            elif node.op.token_type == TOK_SLASH:
                self.emit(('DIV', None))
            elif node.op.token_type == TOK_MOD:
                self.emit(('MOD', None))
            elif node.op.token_type == TOK_CARET:
                self.emit(('EXP', None))
            elif node.op.token_type == TOK_LT:
                self.emit(('LT', None))
            elif node.op.token_type == TOK_GT:
                self.emit(('GT', None))
            elif node.op.token_type == TOK_LE:
                self.emit(('LE', None))
            elif node.op.token_type == TOK_GE:
                self.emit(('GE', None))
            elif node.op.token_type == TOK_EQEQ:
                self.emit(('EQ', None))
            elif node.op.token_type == TOK_NE:
                self.emit(('NE', None))
        elif isinstance(node, UnOp):
            self.compile(node.operand)
            if node.op.token_type == TOK_MINUS:
                self.emit(('NEG', None))
            elif node.op.token_type == TOK_NOT:
                self.emit(('PUSH', (TYPE_NUMBER, 1)))
                self.emit(('XOR', None))
        elif isinstance(node, LogicalOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TOK_AND:
                self.emit(('AND', None))
            elif node.op.token_type == TOK_OR:
                self.emit(('OR', None))
        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.compile(stmt)
        elif isinstance(node, PrintStmt):
            self.compile(node.value)
            if node.end == '\n':
                self.emit(('PRINTLN', None))
            else:
                self.emit(('PRINT', None))

    def generate_code(self, root):
        self.emit(('LABEL', 'START'))
        self.compile(root)
        self.emit(('HALT', None))
        return self.code