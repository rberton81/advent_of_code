import re
from utils.utils import read_input


def get_mul_total(input):
    mul_regex = r"mul\(\d{1,3},\d{1,3}\)"
    numbers_regex = "\d{1,3}"
    total = 0

    for line in read_input(input):
        matches = re.findall(mul_regex, line)

        for mul in matches:
            nb_1, nb_2 = re.findall(numbers_regex, mul)
            total += int(nb_1) * int(nb_2)

    return total


assert get_mul_total("example.txt") == 161
print("solution: ", get_mul_total("input.txt"))
