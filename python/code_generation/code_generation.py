from ast_generation.generated_ast import *
from ast_generation.ast_nodes import *
from inst_types import *

temp_idx = 0

class instList:
    insts = []
    final_temp = ""

    def __init__(self, insts=[]):
        self.insts = insts

    def append(self, instruction):
        self.insts.append(instruction)
        if(instruction.rd != ""):
            self.final_temp = instruction.rd


def alloc_temp():
    global temp_idx
    temp = f"t{temp_idx}"
    temp_idx += 1
    return temp

def generate(IntLit=IntLitNode, insts=instList):
    #utilizing the hardcoded x0 - will be ignored in later register allocation :sob:
    insts.append(addi(alloc_temp, "x0", IntLit.value))

# def generate(Var=VarNode, insts=instList):
#     insts.append(lw())

def generate(BinaryOp=BinaryOpNode, insts=instList):
    #can use addi instead of sequence of add instructions
    if(BinaryOp.op in {"+", "-"} and (type(BinaryOp.left) == IntLitNode or type(BinaryOp.right) == IntLitNode)):
        if(BinaryOp.op == "+"):
            if(type(BinaryOp.left) == IntLitNode):
                generate(BinaryOp.right, insts)
                insts.append(addi(alloc_temp(), insts.final_temp, BinaryOp.left.value))
            elif(type(BinaryOp.right) == IntLitNode):
                generate(BinaryOp.left, insts)
                insts.append(addi(alloc_temp(), insts.final_temp, BinaryOp.right.value))
        elif(BinaryOp.op == "-"):
            if(type(BinaryOp.left) == IntLitNode):
                generate(BinaryOp.right, insts)
                insts.append(addi(alloc_temp(), insts.final_temp, -1 * BinaryOp.left.value))
            elif(type(BinaryOp.right) == IntLitNode):
                generate(BinaryOp.left, insts)
                insts.append(addi(alloc_temp(), insts.final_temp, -1 * BinaryOp.right.value))
    else:
        generate(BinaryOp.left, insts)

        generate(BinaryOp.right, insts)


def generate(StatementList=StatementListNode):
    insts = instList()
    for statement in StatementList.statements:
        generate(statement, insts)