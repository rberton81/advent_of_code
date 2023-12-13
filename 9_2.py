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

        new_first_element = 0
        previous_new_element = 0

        while all_differences:
            last_array = all_differences.pop()
            old_second_element = int(last_array[0])
            new_first_element = old_second_element - previous_new_element
            previous_new_element = new_first_element

        total_sum += new_first_element

    return total_sum


example = read_input("./9_example.txt")
assert get_solution(example) == 2

input = read_input("./9_input.txt")
print("solution", get_solution(input))
