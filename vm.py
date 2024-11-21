from compiler import *
from utils import *
from defs import *
import codecs

# The VM itself consists of a single stack.
#
# Instructions to push and pop from the stack:
#
#      ('PUSH', value)       # Push a value to the stack
#      ('POP',)              # Pop a value from the stack
#
# Stack values are tagged with their type using a tuple:
#
#      (TYPE_NUMBER, 4.0)
#      (TYPE_NUMBER, 15.6)
#      (TYPE_NUMBER, -3.141592)
#      (TYPE_STRING, 'This is a string')
#      (TYPE_BOOL, true)
#
# Instructions to add, subtract, multiply, divide, and compare values from the top of the stack
#
#      ('ADD',)              # Addition
#      ('SUB',)              # Subtraction
#      ('MUL',)              # Multiplication
#      ('DIV',)              # Division
#      ('OR',)               # Bitwise OR
#      ('AND',)              # Bitwise AND
#      ('XOR',)              # Bitwise XOR
#      ('NEG',)              # Negate
#      ('EXP',)              # Exponent
#      ('MOD',)              # Modulo
#      ('EQ',)               # Compare ==
#      ('NE',)               # Compare !=
#      ('GT',)               # Compare >
#      ('GE',)               # Compare >=
#      ('LT',)               # Compare <
#      ('LE',)               # Compare <=
#
# An example of the instruction stream for computing 7 + 2 * 3
#
#      ('PUSH', (TYPE_NUMBER, 7))
#      ('PUSH', (TYPE_NUMBER, 2))
#      ('PUSH', (TYPE_NUMBER, 3))
#      ('MUL',)
#      ('ADD',)
#
# Instructions to load and store variables
#
#      ('LOAD', name)        # Push a global variable name from memory to the stack
#      ('STORE, name)        # Save top of the stack into global variable by name
#      ('LOAD_LOCAL', name)  # Push a local variable name from memory to the stack
#      ('STORE_LOCAL, name)  # Save top of the stack to local variable by name
#
# Instructions to manage control-flow (if-else, while, etc.)
#
#      ('LABEL', name)       # Declares a label
#      ('JMP', name)         # Unconditionally jump to label name
#      ('JMPZ', name)        # Jump to label name if top of stack is zero (or false)
#      ('JSR', name)         # Jump to subroutine/function and keep track of the returning PC
#      ('RTS',)              # Return from subroutine/function

class VM:
    def __init__(self):
        self.stack = []
        self.pc = 0
        self.sp = 0
        self.is_running = False

    def run(self, instructions):
        self.is_running = True
        while self.is_running:
            opcode, *args = instructions[self.pc]
            self.pc += 1
            getattr(self, opcode)(*args)

    def HALT(self):
        self.is_running = False

    def PUSH(self, value):
        if len(self.stack) <= self.sp: self.stack.append(value)
        else: self.stack[self.sp] = value
        self.sp += 1
    
    def POP(self):
        self.sp -= 1
        return self.stack[self.sp]

    def ADD(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, value1 + value2))
        elif type1 == TYPE_STRING or type2 == TYPE_STRING:
            self.PUSH((TYPE_STRING, stringify(value1) + stringify(value2)))
        else:
            vm_error(f'Unsupported operator ADD between {type1} and {type2}', self.pc)

    def SUB(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, value1 - value2))
        else:
            vm_error(f'Unsupported operator SUB between {type1} and {type2}', self.pc)

    def MUL(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, value1 * value2))
        else:
            vm_error(f'Unsupported operator MUL between {type1} and {type2}', self.pc)

    def DIV(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            if value2 == 0:
                vm_error(f'Division by zero')
            self.PUSH((TYPE_NUMBER, value1 / value2))
        else:
            vm_error(f'Unsupported operator DIV between {type1} and {type2}', self.pc)

    def MOD(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            if value2 == 0:
                vm_error(f'Mod by zero')
            self.PUSH((TYPE_NUMBER, value1 % value2))
        else:
            vm_error(f'Unsupported operator MOD between {type1} and {type2}', self.pc)

    def EXP(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, value1 ** value2))
        else:
            vm_error(f'Unsupported operator EXP between {type1} and {type2}', self.pc)

    def AND(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_BOOL and type2 == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, value1 and value2))
        else:
            vm_error(f'Unsupported operator AND between {type1} and {type2}', self.pc)

    def OR(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_BOOL and type2 == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, value1 or value2))
        else:
            vm_error(f'Unsupported operator OR between {type1} and {type2}', self.pc)

    def XOR(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if type1 == TYPE_BOOL and type2 == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, value1 ^ value2))
        elif type1 == TYPE_NUMBER and type2 == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, value1 ^ value2))
        elif (type1 == TYPE_BOOL and type2 == TYPE_NUMBER) or (type1 == TYPE_NUMBER and type2 == TYPE_BOOL):
            self.PUSH((TYPE_BOOL, bool(value1) ^ bool(value2)))
        else:
            vm_error(f'Unsupported operator XOR between {type1} and {type2}', self.pc)

    def EQ(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING) or (type1 == TYPE_BOOL and type2 == TYPE_BOOL):
            self.PUSH((TYPE_BOOL, value1 == value2))
        else:
            vm_error(f'Unsupported operator EQ between {type1} and {type2}', self.pc)

    def NE(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING) or (type1 == TYPE_BOOL and type2 == TYPE_BOOL):
            self.PUSH((TYPE_BOOL, value1 != value2))
        else:
            vm_error(f'Unsupported operator NE between {type1} and {type2}', self.pc)
    
    def GE(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING):
            self.PUSH((TYPE_BOOL, value1 >= value2))
        else:
            vm_error(f'Unsupported operator GE between {type1} and {type2}', self.pc)

    def GT(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING): 
            self.PUSH((TYPE_BOOL, value1 > value2))
        else:
            vm_error(f'Unsupported operator GT between {type1} and {type2}', self.pc)
    
    def LE(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING):
            self.PUSH((TYPE_BOOL, value1 <= value2))
        else:
            vm_error(f'Unsupported operator LE between {type1} and {type2}', self.pc)

    def LT(self):
        type2, value2 = self.POP()
        type1, value1 = self.POP()

        if (type1 == TYPE_NUMBER and type2 == TYPE_NUMBER) or (type1 == TYPE_STRING and type2 == TYPE_STRING):
            self.PUSH((TYPE_BOOL, value1 < value2))
        else:
            vm_error(f'Unsupported operator LT between {type1} and {type2}', self.pc)

    def PRINT(self):
        type, value = self.POP()
        value = stringify(value)
        print(codecs.escape_decode(bytes(value, 'utf-8'))[0].decode('utf-8'), end = '')

    def PRINTLN(self):
        type, value = self.POP()
        value = stringify(value)
        print(codecs.escape_decode(bytes(value, 'utf-8'))[0].decode('utf-8'), end = '\n')

    def NEG(self):
        type, value = self.POP()
        if type == TYPE_NUMBER:
            self.PUSH((type, -value))
        else:
            vm_error(f'Unsupported operator NEG at {type}', self.pc)

    def LABEL(self, name):
        pass