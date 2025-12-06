from utils.utils import read_input
import os 
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))

def solve(input):
    fresh_ranges = set()
    for line in read_input(input):
        if not line:
            break

        current_start, current_end = map(int, line.split("-"))

        to_remove = set()

        for fresh_start, fresh_end in fresh_ranges:
            if fresh_start <= current_end <= fresh_end:
                print(f"merging ({current_start}, {current_end}) into ({fresh_start}, {fresh_end})")
                current_end = max(current_end, fresh_end)
                to_remove.add((fresh_start, fresh_end))
            if fresh_start <= current_start <= fresh_end:
                print(f"merging ({current_start}, {current_end}) into ({fresh_start}, {fresh_end})")
                current_start = min(current_start, fresh_start)
                to_remove.add((fresh_start, fresh_end))
            if fresh_start >= current_start and fresh_end <= current_end:
                print(f"merging ({current_start}, {current_end}) into ({fresh_start}, {fresh_end})")
                to_remove.add((fresh_start, fresh_end))
            
        fresh_ranges.difference_update(to_remove)
        fresh_ranges.add((current_start, current_end))
        print(f"fresh_ranges = {fresh_ranges}")

    fresh_ids_count = 0
    for current_start, current_end in fresh_ranges:
        fresh_ids_count += current_end - current_start + 1
        
    print(f"fresh_ids_count = {fresh_ids_count}")
    return fresh_ids_count
        


assert solve(CURRENT_DIR + "/example.txt") == 14
assert solve(CURRENT_DIR + "/test_case_1.txt") == 6
assert solve(CURRENT_DIR + "/test_case_2.txt") == 10
assert solve(CURRENT_DIR + "/test_case_3.txt") == 6
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")