from tokens import *

class Node:
    pass

class Expr(Node):
    # x + (3 * y)
    pass

class Stmt(Node):
    # perform action (while, if, assign, etc)
    pass

class Integer(Expr):
    # 123
    def __init__(self, value, line):
        assert isinstance(value, int), value
        self.value = value
        self.line = line

class Float(Expr):
    # 3.141592
    def __init__(self, value, line):
        assert isinstance(value, float), value
        self.value = value
        self.line = line

class Bool(Expr):
    # true, false
    def __init__(self, value, line):
        assert isinstance(value, bool), value
        self.value = value
        self.line = line

class String(Expr):
    # true, false
    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line
    
class UnOp(Expr):
    # -x
    def __init__(self, op : Token, operand : Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.op = op
        self.operand = operand
        self.line = line

class BinOp(Expr):
    # x + y
    def __init__(self, op : Token, left : Expr, right : Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

class LogicalOp(Expr):
    def __init__(self, op : Token, left : Expr, right : Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

class Grouping(Expr):
    # ( <Expr> )
    def __init__(self, value, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line

class Stmts(Node):
    # a list of statements
    def __init__(self, stmts, line):
        assert all(isinstance(stmt, Stmt) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line
        
class PrintStmt(Stmt):
    def __init__(self, value : Expr, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line

class WhileStmt(Stmt):
    pass

class Assignment(Stmt):
    pass