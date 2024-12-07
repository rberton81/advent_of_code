from collections import defaultdict
from utils.utils import read_input


def get_number_counts(lines):
    left_number_counts = defaultdict(int)
    right_number_counts = defaultdict(int)
    for line in lines:
        left, right = line.split()

        left_number_counts[int(left)] += 1
        right_number_counts[int(right)] += 1
    return left_number_counts, right_number_counts


def get_similarity_score(left_number_counts, right_number_counts):
    similarity_score = 0
    for number, count in left_number_counts.items():
        similarity_score += number * count * right_number_counts[number]
    return similarity_score


def get_solution(input):
    lines = read_input(input)
    left_number_counts, right_number_counts = get_number_counts(lines)
    solution = get_similarity_score(left_number_counts, right_number_counts)
    return solution


assert get_solution("example.txt") == 31
print("Solution: ", get_solution("input.txt"))
