from utils.utils import read_input


def can_make_design(design, towels, doable_designs, undoable_designs):
    if not design or design in doable_designs:
        return True
    if design in undoable_designs:
        return False

    for i in range(0, len(design)):
        maybe_towel = design[:len(design)-i]
        if maybe_towel in towels:
            if can_make_design(design[len(design)-i:], towels, doable_designs, undoable_designs):
                doable_designs.add(design)
                return True
            
    undoable_designs.add(design)
    return False

def solution(input):
    possible_designs = 0
    towels = []
    designs = []
    for line in read_input(input):
        if "," in line:
            towels += [towel.strip() for towel in line.split(",")]
        else:
            if line.strip():
                designs.append(line.strip())

    doable_designs, undoable_designs = set(), set()
    for design in designs:
        if can_make_design(design, towels, doable_designs, undoable_designs):
            possible_designs += 1
    return possible_designs
    
assert solution("example.txt") == 6
assert solution("example_1.txt") == 1
assert solution("example_2.txt") == 0
_solution = solution("input.txt")
print("solution: ", _solution)