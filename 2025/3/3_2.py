from utils.utils import read_input

def get_max_joltage(joltage, battery_bank, depth):
    max_left= 0
    max_left_index = None
    for index in range(len(battery_bank)-depth):
        left = int(battery_bank[index])
        if left > max_left:
            max_left = left
            max_left_index = index

    joltage += max_left * 10**depth
    battery_bank_remaining = battery_bank[max_left_index+1:]

    if not depth:
        return joltage
    return get_max_joltage(joltage, battery_bank_remaining, depth-1)

def solve(input):
    battery_length = 11
    total_joltage = 0
    for line in read_input(input):
        battery_joltage = get_max_joltage(0, line, battery_length)
        total_joltage += battery_joltage
    return total_joltage

assert solve("example.txt") == 3121910778619

solution = solve("input.txt")
print(f"solution = {solution}")