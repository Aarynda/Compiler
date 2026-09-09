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


class StatementListNode(astNode):
    statements = []

    def __init__(self, statements=[]):
        self.statements = statements

    def append(self, statement):
        self.statements.append(statement)

    def print(self, output_file, tabs):
        for statement in self.statements:
            statement.print(output_file, tabs)