from tokens import *
from model import *
from utils import *

class Paser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def peek(self):
        return self.tokens[self.curr]
        
    def advance(self):
        token = self.peek()
        self.curr = self.curr + 1
        return token

    def is_next(self, expected):
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
            right = self.unary()
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
            expr = BinOp(op, expr, right, op.line)
        return expr

    def or_logical(self):
        expr = self.and_logical()
        while self.match(TOK_OR):
            op = self.previous_token()
            right = self.and_logical()
            expr = BinOp(op, expr, right, op.line)
        return expr

    def expr(self):
        return self.or_logical()

    def parse(self):
        ast = self.expr()
        return ast

            