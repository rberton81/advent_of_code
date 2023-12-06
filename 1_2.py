from utils import STRING_TO_DIGIT, Directions, Tree, read_input


EXAMPLE={
    "two1nine", #29
    "eightwothree", #83
    "abcone2threexyz", #13
    "xtwone3four", #24
    "4nineeightseven2", #42
    "zoneight234", #14
    "7pqrstsixteen", #76
} # sum = 29+83+13+24+42+14+76 = 281


string_digits_tree = Tree(STRING_TO_DIGIT)
STRING_TO_DIGIT_REVERSED = {key[::-1]: value for key, value in STRING_TO_DIGIT.items()}

def get_first_and_last_digits(list):
    first_digit = None
    last_digit = None
    lookup = string_digits_tree.max_lookup_distance

    for index in range(len(list)):
        if not first_digit:
            left = list[index]
            try:
                first_digit = int(left)
            except ValueError:
                path = string_digits_tree.list_is_in_tree_path(
                    list[index:index+lookup]
                )
                if path:
                    first_digit = STRING_TO_DIGIT["".join(path)]

        if not last_digit:
            right = list[-1-index]
            try:
                last_digit = int(right)
            except ValueError:
                path = string_digits_tree.list_is_in_tree_path(
                    list[-1-index:-1-index-lookup:-1], 
                    direction=Directions.LEFT
                )
                if path:
                    last_digit = STRING_TO_DIGIT_REVERSED["".join(path)]

        if first_digit and last_digit:
            return first_digit, last_digit


def get_sum_of_first_and_last_digits(list):
    digits_sum = 0
    for string in list:
        first_digit, last_digit = get_first_and_last_digits(string)
        digits_sum += 10 * first_digit + last_digit
    return digits_sum

assert(get_sum_of_first_and_last_digits(EXAMPLE) == 281)

input = read_input("./1_input.txt")
print('solution', get_sum_of_first_and_last_digits(input))
