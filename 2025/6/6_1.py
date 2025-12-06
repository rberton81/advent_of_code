from utils.utils import read_input
import os 
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))

class Operations:
    SUM = "+"
    PRODUCT = "*"

def solve(input):
    number_groups, operations = [], []
    for line in read_input(input):
        try:
            numbers = []
            for number in line.split(" "):
                if number:
                    numbers.append(int(number))
            number_groups.append(numbers)
        except ValueError:
            for operation in line.split(" "):
                if operation:
                    if operation in (Operations.SUM, Operations.PRODUCT):
                        operations.append(operation)
                    else:
                        raise ValueError(f"Unknown operation: {operation}")

    total_sum = 0
    print("operations:", operations, "number_groups:", number_groups)

    for index, operation in enumerate(operations):
        column = []
        for row in number_groups:
            column.append(row[index])

        if operation == Operations.SUM:
            print(f"adding numbers: {column} for sum: {sum(column)}")
            total_sum += sum(column)
        elif operation == Operations.PRODUCT:
            product = 1
            for number in column:
                product *= number
            print(f"multiplying numbers: {column} for product: {product}")
            total_sum += product
        else:
            raise ValueError(f"Unknown operation: {operation}")

    print(f"total_sum = {total_sum}")
    return total_sum
            


assert solve(CURRENT_DIR + "/example.txt") == 4277556
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")