import os

from utils import read_input

problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def get_arrangements(chars, springs):
    springs_to_fit = "."
    for spring in springs:
        for _ in range(spring):
            springs_to_fit += "#"
        springs_to_fit += "."

    to_fit_dict = {0: 1}
    new_dict = {}

    for char in chars:
        for to_fit in to_fit_dict.keys():
            if char == "?":
                if to_fit + 1 < len(springs_to_fit):
                    new_dict[to_fit + 1] = (
                        new_dict.get(to_fit + 1, 0) + to_fit_dict[to_fit]
                    )
                if springs_to_fit[to_fit] == ".":
                    new_dict[to_fit] = new_dict.get(to_fit, 0) + to_fit_dict[to_fit]

            elif char == ".":
                if (
                    to_fit + 1 < len(springs_to_fit)
                    and springs_to_fit[to_fit + 1] == "."
                ):
                    new_dict[to_fit + 1] = (
                        new_dict.get(to_fit + 1, 0) + to_fit_dict[to_fit]
                    )
                if springs_to_fit[to_fit] == ".":
                    new_dict[to_fit] = new_dict.get(to_fit, 0) + to_fit_dict[to_fit]

            elif char == "#":
                if (
                    to_fit + 1 < len(springs_to_fit)
                    and springs_to_fit[to_fit + 1] == "#"
                ):
                    new_dict[to_fit + 1] = (
                        new_dict.get(to_fit + 1, 0) + to_fit_dict[to_fit]
                    )

        to_fit_dict = new_dict
        new_dict = {}

    return to_fit_dict.get(len(springs_to_fit) - 1, 0) + to_fit_dict.get(
        len(springs_to_fit) - 2, 0
    )


def get_solution(input):
    total_arrangements = 0

    for line in input:
        chars, springs = line.strip().split(" ")
        springs = [int(spring) for spring in springs.split(",")] * 5
        chars = chars + ("?" + chars) * 4
        total_arrangements += get_arrangements(chars, springs)
    return total_arrangements


example_solution = 525152
example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
