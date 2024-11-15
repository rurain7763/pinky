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

class Identifier(Expr):
    # x, PI, _a, start_val, etc...
    def __init__(self, name, line):
        assert isinstance(name, str), name
        self.name = name
        self.line = line

class Stmts(Node):
    # a list of statements
    def __init__(self, stmts, line):
        assert all(isinstance(stmt, Stmt) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line

class PrintStmt(Stmt):
    def __init__(self, value : Expr, end, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.end = end
        self.line = line

class IfStmt(Stmt):
    def __init__(self, condition : Expr, then_stmts : Stmts, else_stmts : Stmts, line):
        assert isinstance(condition, Expr), condition
        assert isinstance(then_stmts, Stmts), then_stmts
        assert else_stmts is None or isinstance(else_stmts, Stmts), else_stmts
        self.condition = condition
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        self.line = line

class WhileStmt(Stmt):
    def __init__(self, condition : Expr, do_stmts : Stmts, line):
        assert isinstance(condition, Expr), condition
        assert isinstance(do_stmts, Stmts), do_stmts
        self.condition = condition
        self.do_stmts = do_stmts
        self.line = line

class Assignment(Stmt):
    def __init__(self, left : Expr, right : Expr, line):
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.left = left
        self.right = right
        self.line = line

class ForStmt(Stmt):
    def __init__(self, assignment : Assignment, condition_val : Expr, step_val : Expr, do_stmts : Stmts, line):
        assert isinstance(assignment, Assignment), assignment
        assert isinstance(condition_val, Expr), condition
        assert step_val is None or isinstance(step_val, Expr), step_val
        assert isinstance(do_stmts, Stmts), do_stmts
        self.assignment = assignment
        self.condition_val = condition_val
        self.step_val = step_val
        self.do_stmts = do_stmts     
        self.line = line   
