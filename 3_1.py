from utils import Map, read_input

example = read_input("./3_example.txt")

one_to_nine = [str(i) for i in range(10)]

def check_symbol_is_around(map, x_start, x_end, y):
    for _y in {y-1, y+1}:
        for x in range(x_start - 1, x_end + 2):
            try:
                char = map[_y][x]
                if char not in one_to_nine and char != ".":
                    return True
            except KeyError:
                continue
            
    for x in {x_start - 1, x_end + 1}:
        try:
            char = map[y][x]
            if char not in one_to_nine and char != ".":
                return True
        except KeyError:
            continue
    return False

def list_number_to_int(list_number):
    int = 0
    for index in range(0, len(list_number)):
        digit = list_number[index]
        int += digit * 10 ** (len(list_number) - index - 1)
    return int

def sum_all_connecting_parts(input):
    map = Map(input)
    number = []
    sum_numbers = 0

    nb_index = 0    
    for y, x__char in map.map.items():
        for x, char in x__char.items():
            if char in one_to_nine:
                number.append(int(char))
            elif number:
                if check_symbol_is_around(map.map, x-len(number), x-1, y):
                    sum_numbers += list_number_to_int(number)
                number = []

        if number :
            if check_symbol_is_around(map.map, x-len(number)+1, x, y):
                sum_numbers += list_number_to_int(number)
            number = []
    return sum_numbers

assert(sum_all_connecting_parts(example) == 4361)

result = sum_all_connecting_parts(read_input("./3_input.txt"))
print('solution', result)