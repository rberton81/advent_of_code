from utils.utils import read_input

def solution(input):
    bytes = []
    for line in read_input(input):
        x, y = line.split()
        bytes.append((x, y))

    
    return len(bytes) 
    

assert solution("example.txt") == 22
_solution = solution("input.txt")
print("solution: ", _solution)