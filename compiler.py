from model import *
from tokens import *
from utils import *
from state import *
from defs import *

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
                self.emit(('ADD',))
            elif node.op.token_type == TOK_MINUS:
                self.emit(('SUB',))
            elif node.op.token_type == TOK_STAR:
                self.emit(('MUL',))
            elif node.op.token_type == TOK_SLASH:
                self.emit(('DIV',))
            elif node.op.token_type == TOK_MOD:
                self.emit(('MOD',))
            elif node.op.token_type == TOK_CARET:
                self.emit(('EXP',))
            elif node.op.token_type == TOK_LT:
                self.emit(('LT',))
            elif node.op.token_type == TOK_GT:
                self.emit(('GT',))
            elif node.op.token_type == TOK_LE:
                self.emit(('LE',))
            elif node.op.token_type == TOK_GE:
                self.emit(('GE',))
            elif node.op.token_type == TOK_EQEQ:
                self.emit(('EQ',))
            elif node.op.token_type == TOK_NE:
                self.emit(('NE',))
        elif isinstance(node, UnOp):
            self.compile(node.operand)
            if node.op.token_type == TOK_MINUS:
                self.emit(('NEG',))
            elif node.op.token_type == TOK_NOT:
                self.emit(('PUSH', (TYPE_NUMBER, 1)))
                self.emit(('XOR',))
        elif isinstance(node, LogicalOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TOK_AND:
                self.emit(('AND',))
            elif node.op.token_type == TOK_OR:
                self.emit(('OR',))
        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.compile(stmt)
        elif isinstance(node, PrintStmt):
            self.compile(node.value)
            if node.end == '\n':
                self.emit(('PRINTLN',))
            else:
                self.emit(('PRINT',))

    def generate_code(self, root):
        self.emit(('LABEL', 'START'))
        self.compile(root)
        self.emit(('HALT',))
        return self.code