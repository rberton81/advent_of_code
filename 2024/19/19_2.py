from collections import defaultdict
from utils.utils import read_input

def get_ways_to_make_designs(design, towels, ways_by_design):
    if not design:
        return 1
    elif design in ways_by_design.keys():
        return ways_by_design[design]

    ways_count = 0
    for i in range(0, len(design)):
        towel_candidate = design[:len(design)-i]
        if towel_candidate in towels:
            sub_design = design[len(design)-i:]
            ways_count += get_ways_to_make_designs(sub_design, towels, ways_by_design)
            
    ways_by_design[design] = ways_count
    return ways_count

def get_towels_and_designs(input):
    towels = []
    designs = []
    for line in read_input(input):
        if "," in line:
            towels += [towel.strip() for towel in line.split(",")]
        else:
            if line.strip():
                designs.append(line.strip())
    return towels, designs

def solution(input):
    towels, designs = get_towels_and_designs(input)
    ways_to_make_designs = 0
    ways_by_design = defaultdict(int)
    for design in designs:
        ways_to_make_designs += get_ways_to_make_designs(design, towels, ways_by_design)
    return ways_to_make_designs
    
assert solution("example.txt") == 16
assert solution("example_3.txt") == 2
_solution = solution("input.txt")
print("solution: ", _solution)