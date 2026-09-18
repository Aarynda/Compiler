class instruction:
    name = ""
    rd = ""
    rs1 = ""
    rs2 = ""
    immediate = 0

    def __init__(self, name):
        self.name = name

    def set_immediate(self, immediate):
        self.immediate = immediate

    def set_rd(self, rd):
        self.rd = rd

    def set_rs1(self, rs1):
        self.rs1 = rs1

    def set_rs2(self, rs2):
        self.rs2 = rs2

class label(instruction):
    def __init__(self, name):
        self.name = name

    def print(self, output_file):
        output_file.write(f"{self.name}:\n")

class itype(instruction):
    def __init__(self, rd, rs1, immediate):
        self.rd = rd
        self.rs1 = rs1
        self.immediate = immediate

    def print(self, output_file):
        output_file.write(f"{self.name} {self.rd}, {self.rs1}, {self.immediate}\n")

class rtype(instruction):
    def __init__(self, rd, rs1, rs2):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def print(self, output_file):
        output_file.write(f"{self.name} {self.rd}, {self.rs1}, {self.rs2}\n")

class stype(instruction):
    def __init__(self, rs1, rs2, immediate):
        self.rs1 = rs1
        self.rs2 = rs2
        self.immediate = immediate

    def print(self, output_file):
        output_file.write(f"{self.name} {self.rs2}, {self.immediate}({self.rs1})\n")

class btype(instruction):
    def __init__(self, rs1, rs2, immediate):
        self.rs1 = rs1
        self.rs2 = rs2
        self.immediate = immediate

    def print(self, output_file):
        if(type(self.immediate) == label):
            output_file.write(f"{self.name} {self.rs1}, {self.rs2}, {self.immediate.name}\n")
        else:
            output_file.write(f"{self.name} {self.rs1}, {self.rs2}, {self.immediate}\n")

class addi(itype):
    name = "addi"

class andi(itype):
    name = "andi"

class xori(itype):
    name = "xori"

class srli(itype):
    name = "srli"

class lw(itype):
    name = "lw"

    def print(self, output_file):
        output_file.write(f"lw {self.rd}, {self.immediate}({self.rs1})\n")

class add(rtype):
    name = "add"

class sub(rtype):
    name = "sub"

class sll(rtype):
    name = "sll"

class sw(stype):
    name = "sw"

class beq(btype):
    name = "beq"

class blt(btype):
    name = "blt"

class ebreak(instruction):
    def __init__(self):
        self.name = "ebreak"

    def print(self, output_file):
        output_file.write(f"{self.name} \n")