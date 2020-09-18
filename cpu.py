"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.fl = '00000000'


    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()
                    if n == '':
                        continue
                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)
                    self.ram[address] = n
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = '00000100'
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = '00000010'
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = '00000001'
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def HLT(self):
        exit()

    def LDI(self, opa, opb):
        self.reg[opa] = opb

    def PRN(self, opa):
        print(self.reg[opa])

    def JMP(self, opa):
        self.pc = self.reg[opa] - 2

    def JEQ(self, opa):
        if self.fl[-1] == '1': 
            self.JMP(opa)

    def JNE(self, opa):
        if self.fl[-1] == '0':
            self.JMP(opa)

    def run(self):
        """Run the CPU."""
        running = True

        while running == True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == 130:
                self.LDI(operand_a, operand_b)
            elif IR == 1:
                self.HLT()
            elif IR == 71:
                self.PRN(operand_a)
            elif IR == 162:
                self.alu('MUL', operand_a, operand_b)
            elif IR == 167:
                self.alu('CMP', operand_a, operand_b)
            elif IR == 84:
                self.JMP(operand_a)
            elif IR == 85:
                self.JEQ(operand_a)
            elif IR == 86:
                self.JNE(operand_a)
            num_ops = (IR & 0b11000000) >> 6
            move_pc_dist = num_ops + 1
            self.pc += move_pc_dist

cp = CPU()
cp.load()
cp.run()