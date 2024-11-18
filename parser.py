from tokens import *
from model import *
from utils import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def peek(self):
        return self.tokens[self.curr]
        
    def advance(self):
        token = self.peek()
        self.curr = self.curr + 1
        return token

    def check(self, expected):
        if self.curr >= len(self.tokens): return False
        return self.peek().token_type == expected

    def expect(self, expected):
        if self.curr >= len(self.tokens):
            parse_error(f'Expected {expected!r}, found EOF', self.previous_token().line)
        elif self.peek().token_type != expected:
            parse_error(f'Expected {expected!r}, found {self.peek().token_type!r}', self.peek().line)
        else:
            return self.advance()

    def match(self, expected):
        if self.curr >= len(self.tokens) or self.peek().token_type != expected: return False
        self.curr = self.curr + 1
        return True

    def previous_token(self):
        return self.tokens[self.curr - 1]

    def primary(self):
        if self.match(TOK_INTEGER): return Integer(int(self.previous_token().lexeme), self.previous_token().line)
        elif self.match(TOK_FLOAT): return Float(float(self.previous_token().lexeme), self.previous_token().line)
        elif self.match(TOK_TRUE): return Bool(True, self.previous_token().line)
        elif self.match(TOK_FALSE): return Bool(False, self.previous_token().line)
        elif self.match(TOK_STRING): return String(self.previous_token().lexeme, self.previous_token().line)
        elif self.match(TOK_LPAREN):
            expr = self.expr()
            if self.match(TOK_RPAREN): return Grouping(expr, self.previous_token().line)
            else: parse_error(f'Error: ")" expected.', self.previous_token().line)
        elif self.match(TOK_IDENTIFIER): 
            identifier = Identifier(self.previous_token().lexeme, self.previous_token().line)
            if self.match(TOK_LPAREN):
                args = []
                while not self.match(TOK_RPAREN):
                    args.append(self.expr())
                    self.match(TOK_COMMA)
                return FuncCall(identifier, args, self.previous_token().line)
            else:
                return identifier

    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand, op.line)
        else:
            return self.primary()

    def exponent(self):
        expr = self.unary()
        while self.match(TOK_CARET): 
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, op.line)
        return expr
    
    def modulo(self):
        expr = self.exponent()
        while self.match(TOK_MOD):
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, op.line)
        return expr

    def multiplication(self):
        expr = self.modulo()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinOp(op, expr, right, op.line)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = BinOp(op, expr, right, op.line)
        return expr
    
    def comparision(self):
        expr = self.addition()
        while self.match(TOK_GT) or self.match(TOK_GE) or self.match(TOK_LT) or self.match(TOK_LE):
            op = self.previous_token()
            right = self.addition()
            expr = BinOp(op, expr, right, op.line)
        return expr

    def equality(self):
        expr = self.comparision()
        while self.match(TOK_NE) or self.match(TOK_EQEQ):
            op = self.previous_token()
            right = self.comparision()
            expr = BinOp(op, expr, right, op.line)
        return expr

    def and_logical(self):
        expr = self.equality()
        while self.match(TOK_AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op, expr, right, op.line)
        return expr

    def or_logical(self):
        expr = self.and_logical()
        while self.match(TOK_OR):
            op = self.previous_token()
            right = self.and_logical()
            expr = LogicalOp(op, expr, right, op.line)
        return expr

    def expr(self):
        return self.or_logical()

    def print_stmt(self, end):
        if self.match(TOK_PRINT) or self.match(TOK_PRINTLN):
            val = self.expr()
            return PrintStmt(val, end, self.previous_token().line)

    def if_stmt(self):
        self.expect(TOK_IF)
        condition = self.expr()
        self.expect(TOK_THEN)
        then_stmts = self.stmts()
        if self.match(TOK_ELSE):
            else_stmts = self.stmts()
        else:
            else_stmts = None
        self.expect(TOK_END)
        return IfStmt(condition, then_stmts, else_stmts, self.previous_token().line)

    def while_stmt(self):
        self.expect(TOK_WHILE)
        condition = self.expr()
        self.expect(TOK_DO)
        do_stmts = self.stmts()
        self.expect(TOK_END)
        return WhileStmt(condition, do_stmts, self.previous_token().line)

    def for_stmt(self):
        self.expect(TOK_FOR)
        assignment = self.stmt()
        self.expect(TOK_COMMA)
        condition_val = self.expr()
        if self.match(TOK_COMMA): step_val = self.expr()
        else: step_val = None
        self.expect(TOK_DO)
        do_stmts = self.stmts()
        self.expect(TOK_END)
        return ForStmt(assignment, condition_val, step_val, do_stmts, self.previous_token().line)

    def func_decl(self):
        self.expect(TOK_FUNC)
        self.expect(TOK_IDENTIFIER)
        name = Identifier(self.previous_token().lexeme, self.previous_token().line)
        self.expect(TOK_LPAREN)
        params = []
        while not self.match(TOK_RPAREN):
            self.expect(TOK_IDENTIFIER)
            params.append(Param(Identifier(self.previous_token().lexeme, self.previous_token().line), self.previous_token().line))
            self.match(TOK_COMMA)
        body_stmts = self.stmts()
        self.expect(TOK_END)
        return FuncDecl(name, params, body_stmts, self.previous_token().line)

    def stmt(self):
        if self.check(TOK_PRINT):
            return self.print_stmt('')
        elif self.check(TOK_PRINTLN):
            return self.print_stmt('\n')
        elif self.check(TOK_IF):
            return self.if_stmt()
        elif self.check(TOK_WHILE):
            return self.while_stmt()
        elif self.check(TOK_FOR):
            return self.for_stmt()
        elif self.check(TOK_FUNC):
            return self.func_decl()
        else:
            left = self.expr()
            if self.match(TOK_ASSIGN):
                right = self.expr()
                return Assignment(left, right, self.previous_token().line)
            else:
                return FuncCallStmt(left)

    def stmts(self):
        stmts = []
        while self.curr < len(self.tokens) and not self.check(TOK_ELSE) and not self.check(TOK_END):
            stmts.append(self.stmt())
        return Stmts(stmts, self.previous_token().line)
    
    def program(self):
        return self.stmts()

    def parse(self):
        return self.program()

            