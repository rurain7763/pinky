from tokens import *

class Expr:
    # x + (3 * y)
    pass

class Stmt:
    # perform action (while, if, assign, etc)
    pass

class Integer(Expr):
    # 123
    def __init__(self, value):
        assert isinstance(value, int), value
        self.value = value
    
    def __repr__(self):
        return f'Integer[{self.value}]'

class Float(Expr):
    # 3.141592
    def __init__(self, value):
        assert isinstance(value, float), value
        self.value = value
    
    def __repr__(self):
        return f'Float[{self.value}]'

class UnOp(Expr):
    # -x
    def __init__(self, op : Token, operand : Expr):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'UnOp({self.op.lexeme!r}, {self.operand})'

class BinOp(Expr):
    # x + y
    def __init__(self, op : Token, left : Expr, right : Expr):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinOp({self.op.lexeme!r}, {self.left}, {self.right})'

class Grouping(Expr):
    # ( <Expr> )
    def __init__(self, value):
        assert isinstance(value, Expr), value
        self.value = value

    def __repr__(self):
        return f'Grouping({self.value})'

class WhileStmt(Stmt):
    pass

class Assignment(Stmt):
    pass