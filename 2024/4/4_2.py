from collections import defaultdict
from utils.utils import read_input

def not_out_of_bounds(x, y, rows):
    return y >= 0 and y < len(rows) and x >= 0 and x < len(rows[0])

def match_diagonal_mas_from_a(rows, x, y):
    counts_by_char = defaultdict(int)

    char_diag_1 = None
    char_diag_2 = None
    for x_direction in (-1, 1):
        for y_direction in (-1, 1):
            new_x = x+x_direction
            new_y = y+y_direction
            if not_out_of_bounds(new_x, new_y, rows):
                char = rows[new_y][new_x]
                counts_by_char[char] += 1
            else:
                return False
            
            # Excludes MAM-SAS
            if x_direction == 1 and y_direction == 1:
                char_diag_1 = char
            if x_direction == -1 and y_direction == -1:
                char_diag_2 = char
            if char_diag_1 and char_diag_2 and char_diag_1 == char_diag_2:
                return False

    if counts_by_char["S"] == 2 and counts_by_char["M"] == 2:
        return True
    
    return False

def find_diagonal_matches(rows):
    matches = 0
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "A":
                matches += match_diagonal_mas_from_a(rows, x, y)
    return matches

def get_x_mas_count(input):
    rows = []
    for line in read_input(input):
        rows.append([char for char in line])

    matches = find_diagonal_matches(rows)

    print(matches)
    return matches

assert get_x_mas_count("example.txt") == 9
print("solution: ", get_x_mas_count("input.txt"))


