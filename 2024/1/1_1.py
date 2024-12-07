from utils.utils import read_input


def get_solution(input):
    left_numbers = []
    right_numbers = []

    for line in read_input(input):
        left, right = line.split()

        left_numbers.append(int(left))
        right_numbers.append(int(right))

    left_numbers.sort()
    right_numbers.sort()

    diff = 0
    for left, right in zip(left_numbers, right_numbers):
        if left != right:
            diff += abs(left - right)
    return diff


assert get_solution("example.txt") == 11
print("solution: ", get_solution("input.txt"))
