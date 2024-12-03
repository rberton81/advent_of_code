import os

from utils import read_input

example_solution = 8410
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def get_empty_rows(input):
    empty_rows = []
    max_y = len(input)
    max_x = len(input[0])

    for y in range(max_y):
        row_is_empty = True
        for x in range(max_x):
            char = input[y][x]
            if char == "#":
                row_is_empty = False
        if row_is_empty:
            empty_rows.append(y)

    return empty_rows


def get_empty_columns(input):
    empty_columns = []
    max_y = len(input)
    max_x = len(input[0])

    for x in range(max_x):
        column_is_empty = True
        for y in range(max_y):
            char = input[y][x]
            if char == "#":
                column_is_empty = False
        if column_is_empty:
            empty_columns.append(x)

    return empty_columns


def get_solution(input, expansion_factor):
    empty_rows = get_empty_rows(input)
    empty_row_count = 0
    empty_columns = get_empty_columns(input)
    empty_column_count = 0

    planet_coordinates = []

    for y, line in enumerate(input):
        if y in empty_rows:
            empty_row_count += 1

        empty_column_count = 0
        for x, char in enumerate(line):
            if x in empty_columns:
                empty_column_count += 1
            if char == "#":
                planet_coordinates.append(
                    (
                        x + empty_column_count * (expansion_factor - 1),
                        y + empty_row_count * (expansion_factor - 1),
                    )
                )

    total_distance = 0

    for current in range(len(planet_coordinates)):
        current_x, current_y = planet_coordinates[current]
        for other in range(current + 1, len(planet_coordinates)):
            other_x, other_y = planet_coordinates[other]
            delta_x = abs(other_x - current_x)
            delta_y = abs(other_y - current_y)
            total_distance += delta_x + delta_y

    return total_distance


example = read_input(f"{problem_id}_example.txt")
expansion_factor = 100
assert get_solution(example, expansion_factor) == example_solution

input = read_input(f"{problem_id}_input.txt")
expansion_factor = 1000000
solution = get_solution(input, expansion_factor)
print(f"solution: {solution}")
