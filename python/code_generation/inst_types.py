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

class itype(instruction):
    def __init__(self, rd, rs1, immediate):
        self.rd = rd
        self.rs1 = rs1
        self.immediate = immediate

    def print(self, output_file):
        output_file.write(f"{self.name} {self.rd}, {self.rs1}, {self.immediate}")

class rtype(instruction):
    def __init__(self, rd, rs1, rs2):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def print(self, output_file):
        output_file.write(f"{self.name} {self.rd}, {self.rs1}, {self.rs2}")

class addi(itype):
    name = "addi"

class add(rtype):
    name = "add"

class sub(rtype):
    name = "sub"
