from utils import read_input

EXAMPLE={
    "1abc2", #12
    "pqr3stu8vwx", #38
    "a1b2c3d4e5f", #15
    "treb7uchet", #77
} # sum = 12+38+15+77 = 142

def get_first_and_last_digits(list):
    first_digit = None
    last_digit = None

    for index in range(len(list)):
        if not first_digit:
            left = list[index]
            try:
                first_digit = int(left)
            except ValueError:
                pass

        if not last_digit:
            right = list[-1-index]
            try:
                last_digit = int(right)
            except ValueError:
                pass

        if first_digit and last_digit:
            return first_digit, last_digit

def get_sum_of_first_and_last_digits(list):
    digits_sum = 0
    for string in list:
        first_digit, last_digit = get_first_and_last_digits(string)
        digits_sum += 10 * first_digit + last_digit
    return digits_sum

assert(get_sum_of_first_and_last_digits(EXAMPLE) == 142)

input = read_input("./1_input.txt")
print('solution', get_sum_of_first_and_last_digits(input))
