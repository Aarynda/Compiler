import sys
sys.path.insert(1, '../ast_generation/')
from functools import singledispatch
from generated_ast import *
from ast_nodes import *
from inst_types import *

SymbolTable = {}
next_addr = 0

def alloc_mem(var=str, varType=str):
    global SymbolTable, next_addr
    match(varType):
        case "int":
            SymbolTable[var] = next_addr
            next_addr += 4 #assuming 4 byte ints
        case "char":
            SymbolTable[var] = next_addr
            next_addr += 1

    print(f"allocating memory for {var}")

temp_idx = 1
label_idx = 0

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
    temp = f"x{temp_idx}"
    temp_idx += 1
    return temp

def alloc_label():
    global label_idx
    label_idx += 1
    return label(f"label{label_idx}")

@singledispatch
def generate(argument, arg2):
    print("erm - howd i get here")

@generate.register(IntLitNode)
def _(IntLit=IntLitNode, insts=instList):
    #utilizing the hardcoded x0 - will be ignored in later register allocation :sob:
    addi_inst = addi(alloc_temp(), "x0", IntLit.value)
    print(type(addi_inst))
    print(type(insts))
    insts.append(addi_inst)

@generate.register(VarNode)
def _(Var=VarNode, insts=instList):
    insts.append(lw(alloc_temp(), "x0", SymbolTable[Var.name])) #for the moment, this one is goofed a little bit rn though

@generate.register(AssignNode)
def _(Assign=AssignNode, insts=instList):
    print("AssignNode")
    generate(Assign.right, insts)
    variable = Assign.var
    if(type(Assign.var) == VarNode):
        variable = Assign.var.name
    insts.append(sw("x0", insts.final_temp, SymbolTable[variable]))

@generate.register(BinaryOpNode)
def _(BinaryOp=BinaryOpNode, insts=instList):
    print("In BinaryOp Node")
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
                insts.append(addi(alloc_temp(), insts.final_temp, "-" + BinaryOp.left.value))
            elif(type(BinaryOp.right) == IntLitNode):
                generate(BinaryOp.left, insts)
                insts.append(addi(alloc_temp(), insts.final_temp, "-" + BinaryOp.right.value))
        # elif(BinaryOp.op == "*"):
        #     if(type(BinaryOp.left) == IntLitNode):
        #         generate(BinaryOp.right, insts)

        #     elif(type(BinaryOp.right) == IntLitNode):
        #         generate(BinaryOp.left, insts)
    else:
        generate(BinaryOp.left, insts)
        left_temp = insts.final_temp
        generate(BinaryOp.right, insts)
        right_temp = insts.final_temp
        match(BinaryOp.op):
            case "+":
                insts.append(add(alloc_temp(), left_temp, right_temp))
            case "-":
                insts.append(sub(alloc_temp(), left_temp, right_temp))
            case "*":
                #Assuming only RV32I - add a check for this later on
                loop_check_reg = alloc_temp()
                output_reg = alloc_temp()
                insts.append(addi(loop_check_reg, "x0", 0))
                insts.append(addi(output_reg, "x0", 0))

                #need way to add label
                loop_label = alloc_label()
                insts.append(loop_label)
                skip_check_reg = alloc_temp()
                insts.append(andi(skip_check_reg, left_temp, 1))

                out_label = alloc_label()
                insts.append(beq(skip_check_reg, "x0", out_label))

                inside_temp = alloc_temp()
                insts.append(add(inside_temp, "x0", right_temp))
                insts.append(sll(inside_temp, inside_temp, loop_check_reg))
                insts.append(add(output_reg, output_reg, inside_temp))

                #place second label
                insts.append(out_label)
                insts.append(srli(left_temp, left_temp, 1))
                last_temp = alloc_temp()
                insts.append(addi(last_temp, "x0", 32))
                insts.append(addi(loop_check_reg, loop_check_reg, 1))
                insts.append(blt(loop_check_reg, last_temp, loop_label))

                insts.append(addi(output_reg, output_reg, 0))



@generate.register(InitializationNode)
def _(Initialization=InitializationNode, insts=instList):
    print("InitializationNode traversal")
    print(f"{Initialization.assignment}")
    variable = ""
    if(type(Initialization.var) == str):
        variable = Initialization.var
    elif(type(Initialization.var) == VarNode):
        variable = Initialization.var.name
    print(f"{variable}, {Initialization.varType}")
    alloc_mem(variable, Initialization.varType)
    if(Initialization.assignment != 0):
        print(type(insts))
        generate(Initialization.assignment, insts)


@generate.register(StatementListNode)
def _(StatementList=StatementListNode):
    print("Traversing StatementListNode")
    insts = instList([])
    print(StatementList.statements)
    for statement in StatementList.statements:
        generate(statement, insts)
        print(type(statement))
    return insts.insts

print(type(StatementList0))
insts = generate(StatementList0)
output_file = open("out.asm", "w")
insts.append(ebreak())
for inst in insts:
    print(inst)
    inst.print(output_file)