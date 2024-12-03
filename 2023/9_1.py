import collections
from utils import read_input


def get_solution(input):
    total_sum = 0

    for line in input:
        array = line.split()

        all_differences = collections.deque([array])
        all_elements_are_zeroes = False

        while not all_elements_are_zeroes:
            deltas = []
            all_elements_are_zeroes = True

            for i in range(len(array) - 1):
                delta = int(array[i + 1]) - int(array[i])
                if delta:
                    all_elements_are_zeroes = False
                deltas.append(delta)

            all_differences.append(deltas)

            array = deltas

        previous_last_element = 0

        while all_differences:
            last_array = all_differences.pop()
            last_element = int(last_array[-1])
            previous_last_element += last_element

        total_sum += previous_last_element

    return total_sum


example = read_input("./9_example.txt")
assert get_solution(example) == 114

input = read_input("./9_input.txt")
print("solution", get_solution(input))
