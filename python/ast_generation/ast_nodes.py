SymbolTable = {}
next_addr = 0

class astNode:
    value = ""

    def __init__(self):
        self.value = ""

class IntLitNode(astNode):
    def __init__(self, value):
        self.value = value

    def print(self, output_file, tabs):
        output_file.write(f"{'  '*tabs}IntLitNode: {self.value}\n")

class VarNode(astNode):
    name = ""

    def __init__(self, name):
        self.name = name

    def print(self, output_file, tabs):
        output_file.write(f"{'  '*tabs}" + f"VarNode: {self.name}\n")

class BinaryOpNode(astNode):
    op = ""
    left = ""
    right = ""

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def print(self, output_file, tabs):
        output_file.write(f"{'  '*tabs}" + f"BinaryOpNode: {self.op}\n")
        self.left.print(output_file, tabs + 1)
        self.right.print(output_file, tabs + 1)

class AssignNode(astNode):
    var = ""
    right = ""

    def __init__(self, var, right):
        self.var = var
        self.right = right

    def print(self, output_file, tabs):
        output_file.write(f"{'  '*tabs}" + "AssignNode:\n")
        self.var.print(output_file, tabs + 1)
        self.right.print(output_file, tabs + 1)

def alloc_mem(var=str, varType=str):
    global SymbolTable, next_addr
    match(varType):
        case "int":
            SymbolTable[var] = next_addr
            next_addr += 4 #assuming 4 byte ints
        case "char":
            SymbolTable[var] = next_addr
            next_addr += 1

class InitializationNode(astNode):
    var = ""
    assignment = 0
    verType = ""

    def __init__(self, assignment, varType=str):
        if(type(assignment) == AssignNode):
            self.var = assignment.var
            self.assignment = assignment
            self.varType = varType
        else:
            self.var = assignment
            self.assignment = 0
            self.varType = varType
        alloc_mem(self.var, varType)

    def print(self, output_file, tabs):
        output_file.write(f"{'  '*tabs}" + "InitializationNode:\n")
        self.var.print(output_file, tabs + 1)
        if(self.assignment != 0):
            self.assignment.print(output_file, tabs + 1)


class StatementListNode(astNode):
    statements = []

    def __init__(self, statements=[]):
        self.statements = statements

    def append(self, statement):
        self.statements.append(statement)

    def print(self, output_file, tabs):
        for statement in self.statements:
            statement.print(output_file, tabs)