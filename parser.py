from token import *
from model import *

class Paser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
    
    def expr(self):
        pass

    def parse(self):
        ast = self.expr()
        return ast