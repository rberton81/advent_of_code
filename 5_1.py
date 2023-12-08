from utils import read_input
import copy


def get_seeds_and_ratios(input):
    sections = [section.strip() for section in input.strip().split("\n\n")]
    seeds_line = sections[0].split(": ")[1]
    seeds = list(map(int, seeds_line.split()))

    ratios = {}

    for section in sections[1:]:
        lines = section.split("\n")
        key = lines[0]
        map_data = [[int(value) for value in line.split()] for line in lines[1:]]
        ratios[key] = map_data
    return seeds, ratios


def get_min_location(input):
    seeds, transaction_name__ratios = get_seeds_and_ratios(input)
    before = {seed: seed for seed in seeds}
    after = {seed: seed for seed in seeds}

    for _, ratios in transaction_name__ratios.items():
        for ratio in ratios:
            destination, source, _range = ratio

            affected_range = (source, source + _range)
            current_seeds = list(before.values())
            affected_seeds = [
                seed
                for seed in current_seeds
                if affected_range[0] <= seed < affected_range[1]
            ]
            seed_delta = destination - source

            for affected_seed in affected_seeds:
                index = list(before.keys())[list(before.values()).index(affected_seed)]
                after[index] += seed_delta

        before = copy.deepcopy(after)

    min_location = min([after[seed] for seed in seeds])
    return min_location


example = read_input("5_example.txt", by_line=False, in_one_line=True)
assert get_min_location(example) == 35

input = read_input("./5_input.txt", by_line=False, in_one_line=True)
print("solution", get_min_location(input))
