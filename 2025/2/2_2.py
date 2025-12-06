from utils.utils import read_input

def is_invalid(product_id):
    repeat_length = 1
    while repeat_length <= len(str(product_id)) // 2:
        sequence = int(str(product_id)[:repeat_length])
        repeated_sequence = int(f"{sequence}{sequence}")
        while True:
            if repeated_sequence < product_id:
                repeated_sequence = int(f"{repeated_sequence}{sequence}")
            elif repeated_sequence > product_id:
                break
            else:
                print(f"{product_id} is invalid")
                return True

        repeat_length += 1

def solve_line(line):
    sum = 0
    for id_range in line.split(","):
        print(f"Looking at range: {id_range}")
        start, end = map(int, id_range.split("-"))
        for product_id in range(int(start), int(end)+1):
            if is_invalid(product_id):
                sum += product_id

    
    print(f"Sum is {sum}")
    return sum

def solve(input):
    sum = 0
    for line in read_input(input):
        sum += solve_line(line)
    return sum

example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
assert solve_line(example) == 4174379265

solution = solve("input.txt")
# 37432260594 ?

