from utils.utils import read_input
import os 
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))

class Operations:
    SUM = "+"
    PRODUCT = "*"

def solve(input):
    lines = []
    for line in read_input(input):
        lines.append([char for char in line if char])
    
    total_sum = 0
    numbers = []
    operations = lines[-1]
    operations.reverse()
    previous_index = -1
    for operation_index, operation in enumerate(operations):
        if operation == ' ':
                continue
        else: 
            number = ""
            for index in range(previous_index, -operation_index-2, -1):
                for line in lines[:-1]:
                    if line[index] != ' ':
                        number += line[index]
                    
                numbers.append(int(number))
                number = ""

            if operation == Operations.SUM:
                for number in numbers:
                    total_sum += number
                numbers = []
            elif operation == Operations.PRODUCT:
                product = 1
                for number in numbers:
                    product *= number
                total_sum += product
                numbers = []
            previous_index = -operation_index-3
    
    return total_sum
            

assert solve(CURRENT_DIR + "/example.txt") == 3263827
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")