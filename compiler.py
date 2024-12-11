from model import *
from tokens import *
from utils import *
from state import *
from defs import *

SYM_VAR = 'SYM_VAR'
SYM_FUNC = 'SYM_FUNC'

class Symbol:
    def __init__(self, name, symtype = SYM_VAR, depth = 0, arg_cnt = 0):
        self.name = name
        self.systype = symtype
        self.depth = depth
        self.arg_cnt = arg_cnt

class Compiler:
    def __init__(self):
        self.code = []
        self.locals = []
        self.globals = []
        self.functions = []
        self.scope_depth = 0
        self.label_counter = 0

    def emit(self, instruction):
        self.code.append(instruction)

    def make_label(self):
        self.label_counter += 1
        return f"LBL{self.label_counter}"
    
    def get_func_symbol(self, name):
        for symbol in reversed(self.functions):
            if(symbol.name == name):
                return symbol
            
        return None
    
    def get_scope_var_symbol(self, name):
        for idx, symbol in reversed(list(enumerate(self.locals))):
            if symbol.depth != self.scope_depth: break
            if symbol.name == name:
                return (symbol, idx)
        
        return (None, None)

    def get_var_symbol(self, name):
        for idx, symbol in reversed(list(enumerate(self.locals))):
            if symbol.name == name:
                return (symbol, idx)

        for idx, symbol in reversed(list(enumerate(self.globals))):
            if symbol.name == name:
                return (symbol, idx)
            
        return (None, None)
    
    def begin_block(self):
        self.scope_depth += 1
    
    def end_block(self):
        i = len(self.locals) - 1
        while i > -1 and self.locals[i].depth == self.scope_depth:
            self.locals.pop()
            self.emit(('POP',))
            i -= 1

        self.scope_depth -= 1

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
        elif isinstance(node, Assignment):
            self.compile(node.right)
            symbol, idx = self.get_var_symbol(node.left.name)
            if not symbol:
                new_symbol = Symbol(node.left.name, SYM_VAR, self.scope_depth)
                if self.scope_depth == 0:
                    self.globals.append(new_symbol)
                    self.emit(('STORE_GLOBAL', len(self.globals) - 1))
                else:
                    self.locals.append(new_symbol)
                    self.emit(('SET_SLOT', (len(self.locals) - 1, node.left.name)))
            else:
                if symbol.depth == 0:
                    self.emit(('STORE_GLOBAL', idx))
                else:
                    self.emit(('STORE_LOCAL', idx))
        elif isinstance(node, LocalAssignment):
            self.compile(node.right)
            symbol, idx = self.get_scope_var_symbol(node.left.name)
            if not symbol:
                new_symbol = Symbol(node.left.name, SYM_VAR, self.scope_depth)
                self.locals.append(new_symbol)
                self.emit(('SET_SLOT', (len(self.locals) - 1, node.left.name)))
            else:
                self.emit(('STORE_LOCAL', idx))
        elif isinstance(node, Identifier):
            symbol, idx = self.get_var_symbol(node.name)
            if not symbol:
                compile_error(f'Variable {node.name} is not defined', node.line)
            else:
                if symbol.depth == 0:
                    self.emit(('LOAD_GLOBAL', idx))
                else:
                    self.emit(('LOAD_LOCAL', idx))
        elif isinstance(node, PrintStmt):
            self.compile(node.value)
            if node.end == '\n':
                self.emit(('PRINTLN',))
            else:
                self.emit(('PRINT',))
        elif isinstance(node, IfStmt):
            self.compile(node.condition)
            then_label = self.make_label()
            else_label = self.make_label()
            exit_label = self.make_label()
            self.emit(('JMPZ', else_label))
            self.emit(('LABEL', then_label))
            self.begin_block()
            self.compile(node.then_stmts)
            self.end_block()
            self.emit(('JMP', exit_label))
            self.emit(('LABEL', else_label))
            if node.else_stmts != None:
                self.begin_block()
                self.compile(node.else_stmts)
                self.end_block()
            self.emit(('LABEL', exit_label))
        elif isinstance(node, WhileStmt):
            cond_label = self.make_label()
            do_label = self.make_label()
            end_label = self.make_label()
            self.emit(('LABEL', cond_label))
            self.compile(node.condition)
            self.emit(('JMPZ', end_label))
            self.emit(('LABEL', do_label))
            self.begin_block()
            self.compile(node.do_stmts)
            self.end_block()
            self.emit(('JMP', cond_label))
            self.emit(('LABEL', end_label))
        elif isinstance(node, ForStmt):
            assign_label = self.make_label()
            cond_label = self.make_label()
            do_label = self.make_label()
            end_label = self.make_label()
            self.emit(('LABEL', assign_label))
            self.begin_block()
            self.compile(node.assignment.right)
            new_symbol = Symbol(node.assignment.left.name, SYM_VAR, self.scope_depth)
            self.locals.append(new_symbol)
            self.emit(('LABEL', cond_label))

            symbol, idx = self.get_var_symbol(node.assignment.left.name)
            cond_val = node.condition_val.value
            if node.step_val != None:
                step_val = node.step_val.value
            else:
                step_val = 1

            self.emit(('LOAD_LOCAL', idx))
            self.emit(('PUSH', (TYPE_NUMBER, cond_val)))
            self.emit(('LE',))
            self.emit(('JMPZ', end_label))
            self.compile(node.do_stmts)
            self.emit(('LOAD_LOCAL', idx))
            self.emit(('PUSH', (TYPE_NUMBER, step_val)))
            self.emit(('ADD',))
            self.emit(('STORE_LOCAL', idx))
            self.emit(('JMP', cond_label))
            self.emit(('LABEL', end_label))
            self.end_block()
        elif isinstance(node, FuncDecl):
            func_symbol = self.get_func_symbol(node.identifier.name)
            if func_symbol:
                compile_error(f'A function with the name {node.identifier.name} was already declared', node.line)
            
            var_symbol, idx = self.get_var_symbol(node.identifier.name)
            if var_symbol:
                compile_error(f'A function with the name {node.identifier.name} was already defined in this scope', node.line)

            new_symbol = Symbol(node.identifier.name, SYM_FUNC, self.scope_depth, len(node.params))
            self.functions.append(new_symbol)
            exit_label = self.make_label()
            self.emit(('JMP', exit_label))
            self.emit(('LABEL', new_symbol.name))

            self.begin_block()
            for parm in node.params:
                new_symbol = Symbol(parm.identifier.name, SYM_VAR, self.scope_depth)
                self.locals.append(new_symbol)
                self.emit(('SET_SLOT', (len(self.locals) - 1, parm.identifier.name)))

            self.compile(node.body_stmts)
            self.end_block()

            self.emit(('PUSH', (TYPE_NUMBER, 0)))
            self.emit(('RTS',))
            self.emit(('LABEL', exit_label))
        elif isinstance(node, FuncCallStmt):
            self.compile(node.func_call)
            self.emit(('POP',))
        elif isinstance(node, FuncCall):
            func_symbol = self.get_func_symbol(node.identifier.name)
            if not func_symbol:
                compile_error(f'A function with the name {node.identifier.name} was not declared', node.line)

            if len(node.args) != func_symbol.arg_cnt:
                compile_error(f'A function with the name {node.identifier.name} expected {func_symbol.arg_cnt} params', node.line)

            for arg in node.args:
                self.compile(arg)

            self.emit(('PUSH', (TYPE_NUMBER, len(node.args))))
            self.emit(('JSR', node.identifier.name))
        elif isinstance(node, RetStmt):
            self.compile(node.value)
            self.emit(('RTS',))

    def generate_code(self, root):
        self.emit(('LABEL', 'START'))
        self.compile(root)
        self.emit(('HALT',))
        return self.code