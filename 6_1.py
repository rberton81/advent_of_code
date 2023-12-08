from utils import read_input
import math

def get_inputs(input):
    times, distances = input
    times = times.split(":")[1].split()
    distances = distances.split(":")[1].split()
    return times, distances

def find_quadratic_roots(a, b, c):
    # Finds roots of quadratic equation ax^2 + bx + c = 0
    discriminant = math.sqrt(b**2 - 4*a*c)

    root1 = (-b + discriminant) / (2*a)
    root2 = (-b - discriminant) / (2*a)

    return root1, root2


def winnings_times(total_time, record):
    # we want t_min so that t_min * (total_time - t_min) > record
    # that gives -t_min^2 + total_time * t_min - record > 0
    root1, root2 = find_quadratic_roots(a = -1, b = int(total_time), c = -int(record))

    lower_bound = min(root1, root2)
    upper_bound = max(root1, root2)

    t_min = math.ceil(lower_bound)
    t_max = math.floor(upper_bound)
    
    winnings_times = t_max - t_min + 1
    # roots excluded (ties don't count)
    if t_min == lower_bound:
        winnings_times -= 1
    if t_max == upper_bound:
        winnings_times -= 1
    
    return winnings_times

def get_solution(input):
    ## EG 7 -> 9, 15 -> 40, 30 -> 200
    times, distances = get_inputs(input)
    solution = 1
    for record, race_time  in zip(times, distances):
        solution *= winnings_times(record, race_time)
    return solution


example = read_input("6_example.txt")
assert(get_solution(example) == 288)


input = read_input("6_input.txt")
print("solution", get_solution(input))