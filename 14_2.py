import collections
import os

example_solution = 64
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]

def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def get_baby(input):
    columns = []
    y = 0

    for _ in range(len(input[0])):    
        columns.append([])

    for line in input:
        x = 0
        for char in line:
            columns[x].append(char)
            x += 1
        y += 1

    return columns

def spin_me_baby(direction, arrays):
    current_weight = 0
    for array in arrays:
        rocks_to_move = 0
        last_rock_y = 0
    
        for idx in range(len(array)):
            char = array[idx]
            if char == "#":
                if rocks_to_move:
                    for i in range(rocks_to_move):
                        array[last_rock_y + i] = "O"
                        if direction == "N":
                            current_weight += len(array) - last_rock_y - i
                    rocks_to_move = 0
                last_rock_y = idx + 1
            elif char == "O":
                array[idx] = "."
                rocks_to_move += 1
        
        if rocks_to_move:
            for i in range(rocks_to_move):
                array[last_rock_y + i] = "O"
            rocks_to_move = 0

    if direction == "E":
        arrays.reverse()
        for array in arrays:
            array.reverse()

    if direction == "S":
        arrays.reverse()

    transposed = [list(transposed) for transposed in zip(*arrays)]
    
    if direction in ["W", "E"]:
        for array in transposed:
            array.reverse()

    if direction == "S":
        transposed.reverse()

    return transposed, current_weight


def print_baby(baby, direction):
    if direction == "E":
        for x in range(len(baby[0])):
            col = []
            for y in range(len(baby)):
                col.append(baby[y][x])
            print(col)
    elif direction =="N":
        for array in baby:
            print(array)
    elif direction =="W":
        for y in range(len(baby)-1,-1,-1):
            array = baby[y]
            print([array[y] for array in baby])
    elif direction == "S":
        for y in range(len(baby)):
            array = baby[y]
            print([array[i] for i in range(len(array)-1, 0, -1)])

def get_weight(baby):
    weight = 0
    for array in baby:
        weight_value = len(baby)
        for char in array:
            if char == "O":
                weight += weight_value
            weight_value -= 1

    return weight

def find_repeating_sequence(array, min_length=4):
    sequence_length = min_length
    max_length = len(array) // 2

    while sequence_length <= max_length:
        for i in range(len(array) - 2 * sequence_length + 1):
            if array[i:i + sequence_length] == array[i + sequence_length:i + 2 * sequence_length]:
                return array[i:i + sequence_length]
        sequence_length += 1
    return None

def get_solution(input):
    baby = get_baby(input)
    max_cycles = 1000000000
    weights = []

    for cycle in range(max_cycles):
        for direction in ["N", "W", "S", "E"]:
            baby, weight = spin_me_baby(direction, baby)
        
        weight = get_weight(baby)
        weights.append(weight)

        if cycle == 10000:
            sequence = find_repeating_sequence(weights)

            if sequence:
                for idx, weight in enumerate(weights):
                    if weight == sequence[0]:
                        is_solution = True
                        for i in range(len(sequence)):
                            print(f"i {i}")
                            if weights[idx+i] != sequence[i]:
                                is_solution = False
                                break
                        if is_solution:
                            buffer = idx
                            break

            def get_final_weight(max_cycles):
                cycles_in_loop = max_cycles - buffer
                modulo = cycles_in_loop % (len(sequence))
                answer = sequence[modulo-1]
                return answer

            solution = get_final_weight(max_cycles)
            return solution

    total_weight = 0
    return total_weight

example = read_input(f"{problem_id}_example.txt")
assert(get_solution(example) == example_solution)

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")