from utils.utils import read_input

class Direction:
    LEFT = "L"
    RIGHT = "R"

def solve(input):
    position = 50
    zeroes_count = 0

    for line in read_input(input):
        direction = line[0]
        distance = int(line[1:]) % 100
        if direction == Direction.LEFT:
            position -= distance
            if position < 0:
                position += 100
        elif direction == Direction.RIGHT:
            position += distance
            position = position % 100
            
        if position == 0:
            zeroes_count += 1

    assert zeroes_count > 992

solve("input.txt")