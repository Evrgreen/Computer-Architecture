
"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
POP = 0b01000110
PUSH = 0b01000101
MUL = 0b10100010
ADD = 0b10100000
DIV = 0b10100011
SUB = 0b10100001
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.register[SP] = 0xF4
        self.process_table = {
            LDI : self.ldi,
            PRN : self.prn,
            HLT : self.hlt,
            POP : self.pop,
            PUSH: self.push,
            MUL : self.alu,
            ADD : self.alu,
            DIV : self.alu,
            SUB : self.alu
        }

    def ldi(self, op_a, op_b):
        self.register[op_a] = op_b 
    
    def prn(self, op_a, op_b=None):
        print(self.register[op_a])

    def hlt(self, op_a, op_b=None):
        sys.exit()
    
    def pop(self, op_a, op_b=None):
        value = self.ram_read(self.register[SP])
        self.register[op_a] = value
        self.register[SP] += 1
        return value
    
    def push(self, op_a, op_b=None):
        self.register[SP] -= 1
        self.ram_write(self.register[SP], self.register[op_a])
        
    def load(self, filename):
        """Load a program into memory."""
        address = 0

        with open(filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                self.ram[address] = int(line, 2)      
                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.register[reg_a] += self.register[reg_b]
        elif op == SUB:
            self.register[reg_a] -= self.register[reg_b]
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        elif op == DIV:
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, mar):
        '''
        Takes address (mar) in ram and returns the value (mdr) stored there
        '''
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mar, mdr):
        '''
        Stores 'value' (MDR) at given 'address' (MAR) in ram
        '''
        self.ram[mar] = mdr

    def run(self):
        '''
        Run the CPU
        '''
        while True:
            ir = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            run_counter = (ir >> 6) + 1
            alu_op = bool(((ir >> 5) & 0b1))  
            if ir in self.process_table:
                if alu_op:
                    self.process_table[ir](ir, op_a, op_b)
                else:
                    self.process_table[ir](op_a, op_b)
            else:
                print('Unsupported operation')
            self.pc += run_counter
    

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

