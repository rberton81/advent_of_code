from utils.utils import read_input

def calculate_next_secret(current_secret):
    current_secret = (current_secret * 64) ^ current_secret
    current_secret = current_secret % 16777216
    current_secret = (current_secret // 32) ^ current_secret
    current_secret = current_secret % 16777216
    current_secret = (current_secret * 2048) ^ current_secret
    current_secret = current_secret % 16777216
    return current_secret

def solution(input):
    sum = 0
    for line in read_input(input):
        next_secret = None 
        for _ in range(2000):
            next_secret = calculate_next_secret(next_secret or int(line))
        sum += next_secret
    return sum


assert solution("example.txt") == 37327623
_solution = solution("input.txt")
print("solution: ", _solution)
