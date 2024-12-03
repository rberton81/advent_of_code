import os

example_solution = 1320
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def get_hash(char, current_value):
    ascii_code = ord(char)
    current_value += ascii_code
    current_value *= 17
    current_value %= 256
    return current_value


def get_solution(input):
    strings = input.split(",")
    total_sum = 0
    for string in strings:
        current_value = 0
        for char in string:
            current_value = get_hash(char, current_value)
        total_sum += current_value

    return total_sum


assert get_solution("HASH") == 52
example = read_input(f"{problem_id}_example.txt")
assert get_solution(example[0]) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input[0])
print(f"solution: {solution}")
