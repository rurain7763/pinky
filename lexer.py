from tokens import *
from utils import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []
        pass

    def advance(self):
        ch = self.source[self.curr]
        self.curr = self.curr + 1
        return ch
    
    def peek(self):
        return self.source[self.curr]
    
    def lookahead(self, n = 1):
        if self.curr >= len(self.source): return '\0'
        return self.source[self.curr + n]
    
    def match(self, expected):
        if self.curr >= len(self.source):
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1
        return True
    
    def add_token(self, token_type):
        self.tokens.append(Token(token_type, self.source[self.start:self.curr], self.line))

    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            if ch == '\n': self.line = self.line + 1
            elif ch == '\r': pass
            elif ch == '\t': pass
            elif ch == ' ': pass
            elif ch == '(': self.add_token(TOK_LPAREN)
            elif ch == ')': self.add_token(TOK_RPAREN)
            elif ch == '{': self.add_token(TOK_LCURLY)
            elif ch == '}': self.add_token(TOK_RCURLY)
            elif ch == '[': self.add_token(TOK_LSQUAR)
            elif ch == ']': self.add_token(TOK_RSQUAR)
            elif ch == '.': self.add_token(TOK_DOT)
            elif ch == ',': self.add_token(TOK_COMMA)
            elif ch == '+': self.add_token(TOK_PLUS)
            elif ch == '-':
                if self.match('-'):
                    while self.curr < len(self.source) and self.peek() != '\n':
                        self.advance()
                else: 
                    self.add_token(TOK_MINUS)
            elif ch == '*': self.add_token(TOK_STAR)
            elif ch == '^': self.add_token(TOK_CARET)
            elif ch == '/': self.add_token(TOK_SLASH)
            elif ch == ';': self.add_token(TOK_SEMICOLON)
            elif ch == '?': self.add_token(TOK_QUESTION)
            elif ch == '%': self.add_token(TOK_MOD)
            elif ch == '=':
                if self.match('='): self.add_token(TOK_EQEQ)
                else: self.add_token(TOK_EQ)
            elif ch == ':':
                if self.match('='): self.add_token(TOK_ASSIGN)
                else: self.add_token(TOK_COLON)
            elif ch == '<':
                if self.match('='): self.add_token(TOK_LE)
                elif self.match('<'): self.add_token(TOK_LTLT)
                else: self.add_token(TOK_LT)
            elif ch == '>':
                if self.match('='): self.add_token(TOK_GE)
                elif self.match('>'): self.add_token(TOK_GTGT)
                else: self.add_token(TOK_GT)
            elif ch == '~':
                if self.match('='): self.add_token(TOK_NE)
                else: self.add_token(TOK_NOT)
            elif ch.isdigit():
                dot_cnt = 0
                while self.curr < len(self.source) and (self.peek().isdigit() or self.peek() == '.'):
                    if self.peek() == '.': dot_cnt = dot_cnt + 1
                    self.advance()

                if dot_cnt == 0: self.add_token(TOK_INTEGER)
                elif dot_cnt == 1: self.add_token(TOK_FLOAT)
            elif ch == '\"' or ch == '\'':
                while self.curr < len(self.source) and self.peek() != ch:
                    self.advance()
                
                if(self.peek() == ch):
                    self.start = self.start + 1
                    self.add_token(TOK_STRING)
                    self.advance()
            elif ch.isalpha() or ch == '_':
                while self.curr < len(self.source) and (self.peek().isalnum() or self.peek() == '_'):
                    self.advance()

                keyword = keywords.get(self.source[self.start:self.curr])
                if keyword == None: self.add_token(TOK_IDENTIFIER)
                else: self.add_token(keyword)
            else:
                lexeing_error(f"Error at {ch!r}: Unexpected character", self.line)
        
        return self.tokens
            
        
        
