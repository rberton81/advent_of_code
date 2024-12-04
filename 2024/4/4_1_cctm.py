import re
from utils.utils import read_input

XMAS_REGEX = r'XMAS'
SAMX_REGEX = r'SAMX'
XMAS = "XMAS"

def transpose(list_of_lists):
    return list(map(list, zip(*list_of_lists)))

def find_horizontal_matches(columns):
    matches = 0
    for column in columns:
        matches += len(re.findall(XMAS_REGEX, "".join(column)))
        matches += len(re.findall(SAMX_REGEX, "".join(column)))
    return matches

def find_vertical_matches(rows):
    matches = 0
    for row in rows:
        matches += len(re.findall(XMAS_REGEX, "".join(row)))
        matches += len(re.findall(SAMX_REGEX, "".join(row)))
    return matches

def not_out_of_bounds(x, y, rows):
    return y >= 0 and y < len(rows) and x >= 0 and x < len(rows[0])

def match_diagonal_xmas_from_x(rows, x, y):
    matches = 0
    for x_direction in (-1, 1):
        for y_direction in (-1, 1):
            offset = 1
            maybe_xmas = "X"
            while maybe_xmas in XMAS:
                new_x = x+x_direction*offset
                new_y = y+y_direction*offset
                if not_out_of_bounds(new_x, new_y, rows):
                    maybe_xmas += rows[new_y][new_x]
                else:
                    maybe_xmas = "NOT_XMAS!"
                if maybe_xmas == XMAS:
                    matches += 1
                offset += 1
    return matches

def find_diagonal_matches(rows):
    matches = 0
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "X":
                matches += match_diagonal_xmas_from_x(rows, x, y)
    return matches
        

def get_xmas_count(input):
    rows = []
    for line in read_input(input):
        rows.append([char for char in line])

    matches = find_horizontal_matches(rows) + find_vertical_matches(transpose(rows)) + find_diagonal_matches(rows)

    print(matches)
    return matches

assert get_xmas_count("example.txt") == 18
print("solution: ", get_xmas_count("input.txt"))


