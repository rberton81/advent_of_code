import collections
import os

from utils import read_input

example_solution = 136
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def get_rock_map_and_columns(input):
    columns = collections.defaultdict(list)
    y = 0
    for line in input:
        x = 0
        for char in line:
            columns[x].append(char)
            x += 1
        y += 1

    return columns


def get_solution(input):
    columns = get_rock_map_and_columns(input)
    total_weight = 0

    for column in columns.values():
        rocks_to_move = 0
        y = 0
        last_rock_y = 0

        for char in column:
            if char == "#":
                if rocks_to_move:
                    for i in range(rocks_to_move):
                        total_weight += len(column) - last_rock_y - i
                    rocks_to_move = 0
                last_rock_y = y + 1
            elif char == "O":
                rocks_to_move += 1
            y += 1

        if rocks_to_move:
            for i in range(rocks_to_move):
                total_weight += len(column) - last_rock_y - i
            rocks_to_move = 0

    return total_weight


example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
