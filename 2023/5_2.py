from utils import read_input
import numpy as np
import concurrent.futures


def get_seeds_and_ratios(input):
    sections = [section.strip() for section in input.strip().split("\n\n")]
    seeds_line = sections[0].split(": ")[1]
    seeds_config = list(map(int, seeds_line.split()))

    mappings = {}

    for section in sections[1:]:
        lines = section.split("\n")
        transition = lines[0]
        mapping = [[int(value) for value in line.split()] for line in lines[1:]]
        mappings[transition] = mapping

    return seeds_config, mappings


def process_seeds(seeds, mappings):
    before = np.copy(seeds)
    after = np.copy(seeds)

    for mapping in mappings:
        for destination, source, _range in mapping:
            left_bound, right_bound = (source, source + _range)
            seed_is_mapped = np.logical_and(left_bound <= before, before < right_bound)
            after[seed_is_mapped] += destination - source
        before = np.copy(after)

    return np.min(after)


def get_min_location(input):
    num_threads = 8
    chunk_size = 100000

    seeds_config, transaction_name__ratios = get_seeds_and_ratios(input)
    ratios = list(transaction_name__ratios.values())
    location_min = float("inf")

    for seed_base, seed_count in zip(seeds_config[::2], seeds_config[1::2]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            seed_futures = []
            seeds = np.arange(seed_base, seed_base + seed_count)

            for i in range(0, len(seeds), chunk_size):
                seeds_chunk = seeds[i : i + chunk_size]
                seed_futures.append(executor.submit(process_seeds, seeds_chunk, ratios))

            for future in concurrent.futures.as_completed(seed_futures):
                local_min = future.result()
                if local_min < location_min:
                    location_min = local_min
    return location_min


example = read_input("5_example.txt", by_line=False, in_one_line=True)
assert get_min_location(example) == 46

input = read_input("./5_input.txt", by_line=False, in_one_line=True)
print("solution", get_min_location(input))
