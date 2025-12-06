from utils.utils import read_input
import os 
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))

def solve(input):
    fresh_ingredients = 0
    fresh_ranges = []
    processing_fresh_food_ranges = True
    for line in read_input(input):
        if not line:
            processing_fresh_food_ranges = False
            continue

        if processing_fresh_food_ranges:
            start, end = map(int, line.split("-"))
            fresh_ranges.append((start, end))
        else:
            ingredient = int(line)
            for start, end in fresh_ranges:
                if start <= ingredient <= end:
                    print(f"ingredient {ingredient} is fresh in range ({start}, {end})")
                    fresh_ingredients += 1
                    break
                
    print(f"fresh_ingredients = {fresh_ingredients}")
    return fresh_ingredients
        


assert solve(CURRENT_DIR + "/example.txt") == 3
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")