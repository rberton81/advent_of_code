from utils.utils import read_input


class Direction:
    LEFT = "L"
    RIGHT = "R"

def solve(input):
    position = 50
    zeroes_count = 0

    for line in read_input(input):
        direction = line[0]
        distance = int(line[1:])
        full_rotations = distance // 100
        zeroes_count += full_rotations
        distance = distance % 100
        position__before = position

        if direction == Direction.LEFT:
            position -= distance
            if position == 0:
                zeroes_count += 1
            elif position < 0:
                position += 100
                if not position__before == 0:
                    zeroes_count += 1
        elif direction == Direction.RIGHT:
            position += distance
            if position > 99:
                position -= 100
                zeroes_count += 1

solve("input.txt")