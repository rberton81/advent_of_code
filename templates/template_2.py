import os

example_solution = 99999999
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def get_solution(input):
    ##TODO write me ;)
    pass


example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
