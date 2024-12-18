from utils.utils import read_input


def get_button(line):
    x_a, y_a = line.split()[-2:]
    x_a = int(x_a.split("+")[1].strip(","))
    y_a = int(y_a.split("+")[1].strip(","))
    return x_a, y_a


def get_prize(line):
    x_prize, y_prize = line.split()[-2:]
    x_prize = int(x_prize.split("=")[1].strip(","))
    y_prize = int(y_prize.split("=")[1].strip(","))
    return x_prize, y_prize


def solve(x_a, y_a, x_b, y_b, x_prize, y_prize):
    # we press button A n times and button B m times
    denom = x_a * y_b - x_b * y_a
    n = (y_b * x_prize - x_b * y_prize) // denom
    m = (y_prize * x_a - x_prize * y_a) // denom

    if n <= 100 and m <= 100 and n >= 0 and m >= 0:
        x_adds_up = n * x_a + m * x_b == x_prize
        y_adds_up = n * y_a + m * y_b == y_prize
        if x_adds_up and y_adds_up:
            return 3 * n + m
    return 0


def solution(input):
    total_price = 0

    idx = 0
    for line in read_input(input):
        if idx % 4 == 0:
            x_a, y_a = get_button(line)
        elif idx % 4 == 1:
            x_b, y_b = get_button(line)
        elif idx % 4 == 2:
            x_prize, y_prize = get_prize(line)
        else:
            total_price += solve(x_a, y_a, x_b, y_b, x_prize, y_prize)
        idx += 1

    return total_price


assert solution("example.txt") == 480
_solution = solution("input.txt")
print("solution: ", _solution)
