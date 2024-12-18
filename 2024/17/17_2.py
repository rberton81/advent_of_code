from collections import deque
from utils.utils import read_input

# Combo operands 0 through 3 represent literal values 0 through 3.
# Combo operand 4 represents the value of register A.
# Combo operand 5 represents the value of register B.
# Combo operand 6 represents the value of register C.
# Combo operand 7 is reserved and will not appear in valid programs.

class InstructionJump(Exception):
    def __init__(self, jump_to):
        self.jump_to = jump_to
        

class REGISTERS:
    A = "A"
    B = "B"
    C = "C"

class Operand:
        def __init__(self, id):
            self.id = id

        def combo(self, registers):
            if self.id <= 3:
                return self.id
            elif self.id == 4:
                return registers[REGISTERS.A]
            elif self.id == 5:
                return registers[REGISTERS.B]
            elif self.id == 6:
                return registers[REGISTERS.C]
            else:
                raise ValueError(f"Invalid operand_id: {self.id}")

        def literal(self):
            return int(self.id)
        
        def __repr__(self):
            return f"Operand({self.id})"
            
def adv(registers, operand):
    div = registers[REGISTERS.A] // 2**operand.combo(registers)
    registers[REGISTERS.A] = div

def bxl(registers, operand):
    xor = registers[REGISTERS.B] ^ operand.literal()
    registers[REGISTERS.B] = xor

def bst(registers, operand):
    modulo = operand.combo(registers) % 8
    registers[REGISTERS.B] = modulo

def jnz(registers, operand):
    if registers[REGISTERS.A] != 0:
        raise InstructionJump(operand.literal())

def bxc(registers, operand):
    xor = registers[REGISTERS.B] ^ registers[REGISTERS.C]
    registers[REGISTERS.B] = xor

def out(registers, operand):
    return operand.combo(registers) % 8

def bdv(registers, operand):
    div = registers[REGISTERS.A] // 2**operand.combo(registers)
    registers[REGISTERS.B] = div

def cdv(registers, operand):
    div = registers[REGISTERS.A] // 2**operand.combo(registers)
    registers[REGISTERS.C] = div

def execute_instruction(opcode, operand, registers):
    if opcode == 0:
        result= adv(registers, operand)
    elif opcode == 1:
        result= bxl(registers, operand)
    elif opcode == 2:
        result= bst(registers, operand)
    elif opcode == 3:
        result= jnz(registers, operand)
    elif opcode == 4:
        result= bxc(registers, operand)
    elif opcode == 5:
        result= out(registers, operand)
    elif opcode == 6:
        result= bdv(registers, operand)
    elif opcode == 7:
        result= cdv(registers, operand)
    return str(result) if result is not None else ""

def test_value(value, instructions, program, registers):
    registers[REGISTERS.A] = value
    instruction_pointer = 0
    output = ""
    try:
        while True:
            opcode = instructions[instruction_pointer]
            operand = Operand(instructions[instruction_pointer + 1])
            try:
                output += execute_instruction(opcode, operand, registers)
                instruction_pointer += 2
            except InstructionJump as e:
                instruction_pointer = e.jump_to
    except IndexError:
        print("Halt", program, output)
        return output

def solution(input):
    registers = {}
    for line in read_input(input):
        if "Register" in line:
            register, count = line.split(":")
            register_id = register.split()[1]
            count = int(count)
            registers[register_id]=count
        elif "Program" in line:
            program = line.split(":")[1].strip()
            instructions = [int(char) for char in program.split(",")]
    
    print(f"instructions: {instructions}")
    init_state = registers

    # tested_value = 203147121000000
    tested_value = 140000000000000
    #TODO value has same amount of digits

    # value_digits_count = len(program.split(","))
    # _tested_value = 203147121262590 ##TODO
    _tested_value = 203147121000000 ##TODO
    value_digits_count = len(str(_tested_value))
    tested_digit_idx = 9
    #TODO change 2nd and 3rd number until last digit match
    
    # for i in range(1, 10):
    #     # for j in range(0, 10):
    #         # print(f"i, j: {i}, {j}")
    #         # tested_value = _tested_value+ i*10**(value_digits_count-tested_digit_idx) + j*10**(value_digits_count-tested_digit_idx-1)
    #     tested_value = _tested_value+ i*10**(value_digits_count-tested_digit_idx)

    #     while True:
    #         registers = init_state
    #         print(f"Testing {tested_value}")
    #         output = test_value(tested_value, instructions, program, registers)
    #         # import pdb; pdb.set_trace() #TODO
    #         observed = ",".join(output)
    #         if observed == program:
    #             print("OK!", tested_value)
    #             return tested_value
    #         else:
    #             print(f'Nope, next: {tested_value} -> {observed} / {program}')
    #             import pdb; pdb.set_trace()
    #             break
    #             # tested_value += 1

    while True:
        registers = init_state
        print(f"Testing {tested_value}")
        output = test_value(tested_value, instructions, program, registers)
        # import pdb; pdb.set_trace() #TODO
        observed = ",".join(output)
        if observed == program:
            print("OK!", tested_value)
            return tested_value
        else:
            print(f'Nope, next: {tested_value} -> {observed} / {program}')
            tested_value += 512*10000000000
            import pdb; pdb.set_trace()

# assert solution("example_1.txt") == 117440
_solution = solution("input.txt")
print("solution: ", _solution)