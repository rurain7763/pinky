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
        if self.match(TOK_INTEGER): return Integer(int(self.previous_token().lexeme))
        elif self.match(TOK_FLOAT): return Float(float(self.previous_token().lexeme))
        elif self.match(TOK_LPAREN):
            expr = self.expr()
            if self.match(TOK_RPAREN): return Grouping(expr)
            else: parse_error(f'Error: ")" expected.', self.previous_token().line)

    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand)
        else:
            return self.primary()

    def factor(self):
        return self.unary()
        
    def term(self):
        expr = self.factor()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.previous_token()
            right = self.factor()
            expr = BinOp(op, expr, right)
        return expr

    def expr(self):
        expr = self.term()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.previous_token()
            right = self.term()
            expr = BinOp(op, expr, right)
        return expr

    def parse(self):
        ast = self.expr()
        return ast

            