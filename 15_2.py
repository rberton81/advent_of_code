import collections
import os

example_solution = 145
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def get_hash(string):
    current_value = 0
    for char in string:
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= 17
        current_value %= 256
    return current_value


def get_focusing_power(boxes, label_by_focus_power):
    focusing_power = 0
    for box_nb, box in boxes.items():
        for slot, label in enumerate(box):
            focusing_power += (1 + box_nb) * (slot + 1) * label_by_focus_power[label]
    return focusing_power


def get_solution(input):
    boxes = collections.defaultdict(list)
    label_by_focus_power = {}
    strings = input.split(",")

    for string in strings:
        if "=" in string:
            label, lense_nb = string.split("=")

            label_by_focus_power[label] = int(lense_nb)
            box_nb = get_hash(label)

            box = boxes[box_nb]
            if not label in box:
                box.append(label)

        elif "-" in string:
            label = string.split("-")[0]

            box_nb = get_hash(label)
            box = boxes[box_nb]
            if label in box:
                box.remove(label)

    return get_focusing_power(boxes, label_by_focus_power)


example = read_input(f"{problem_id}_example.txt")
assert get_solution(example[0]) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input[0])
print(f"solution: {solution}")
