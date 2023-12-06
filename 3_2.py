import collections
from utils import Map, read_input

example = read_input("./3_example.txt")

one_to_nine = [str(i) for i in range(10)]

def check_symbol_is_around(map, x_start, x_end, y):
    positions = []
    for _y in {y-1, y+1}:
        for x in range(x_start - 1, x_end + 2):
            try:
                char = map[_y][x]
                if char == "*":
                    positions.append((x, _y))
            except KeyError:
                continue
            
    for x in {x_start - 1, x_end + 1}:
        try:
            char = map[y][x]    
            if char == "*":
                positions.append((x, y))
        except KeyError:
            continue
    return positions

def list_number_to_int(list_number):
    int = 0
    for index in range(0, len(list_number)):
        digit = list_number[index]
        int += digit * 10 ** (len(list_number) - index - 1)
    return int

def add_number_to_gear_map(map, gear_map, number, x, y, number_was_at_border=False):
    if number_was_at_border:
            symbol_positions = check_symbol_is_around(map, x-len(number)+1, x, y)
    else:
        symbol_positions = check_symbol_is_around(map, x-len(number), x-1, y)
    if symbol_positions:
        for symbol_position in symbol_positions: 
            x_symb, y_symb = symbol_position
            try:
                gear_map[y_symb][x_symb].append(list_number_to_int(number))
            except KeyError:
                gear_map[y_symb] = collections.defaultdict(list)
                gear_map[y_symb][x_symb].append(list_number_to_int(number))
    return gear_map

def sum_all_connecting_parts(input):
    map = Map(input)
    gear_map = collections.defaultdict(collections.defaultdict)
    number = []
    sum = 0

    for y, x__char in map.map.items():
        for x, char in x__char.items():
            if char in one_to_nine:
                number.append(int(char))
            elif number:
                gear_map = add_number_to_gear_map(map.map, gear_map, number, x, y)
                number = []

        if number :
            gear_map = add_number_to_gear_map(map.map, gear_map, number, x, y, number_was_at_border=True)
            number = []

    for y, x_values in gear_map.items():
        for x, numbers_list in x_values.items():
            if len(numbers_list) == 2:
                sum += numbers_list[0] * numbers_list[1]
    return sum

assert(sum_all_connecting_parts(example) == 467835)

result = sum_all_connecting_parts(read_input("./3_input.txt"))
print('solution', result)