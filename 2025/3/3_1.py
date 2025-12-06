from utils.utils import read_input

def get_max_joltage(battery_bank):
    print(f"Looking at bank: {battery_bank}")
    max_left, max_right = 0, 0
    max_left_index = None
    for index in range(len(battery_bank)-1):
        left = int(battery_bank[index])
        if left > max_left:
            max_left = left
            max_left_index = index

    battery_bank_remaining = battery_bank[max_left_index+1:]
    for index in range(len(battery_bank_remaining)):
        right = int(battery_bank_remaining[-(index+1)])
        if right > max_right:
            max_right = right

    print(f"Max left: {max_left}, Max right: {max_right}")
    return max_left * 10 + max_right


def solve(input):
    sum = 0
    for line in read_input(input):
        sum += get_max_joltage(line)
    return sum

assert solve("example.txt") == 357

solution = solve("input.txt")
print(f"solution = {solution}")