import re
from utils.utils import read_input

DO = "do()"
DONT = "don't()"

def get_mul_total(input):
    instruction_regex = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    numbers_regex = "\d{1,3}"
    total = 0

    should_multiply = True
    for instructions in read_input(input):
        matched_instructions = re.findall(instruction_regex, instructions)

        for instruction in matched_instructions:
            if instruction == DO:
                should_multiply = True
            elif instruction == DONT:
                should_multiply = False
            else:
                if should_multiply:
                    nb_1, nb_2 = re.findall(numbers_regex, instruction)
                    total += int(nb_1) * int(nb_2)

    return total


assert get_mul_total("example_2.txt") == 48
print("solution: ", get_mul_total("input.txt"))


