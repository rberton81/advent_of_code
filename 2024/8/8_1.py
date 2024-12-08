import collections
from utils.utils import read_input


class Antinode:
    def __init__(self, antenna_1, antenna_2):
        x_vector, y_vector = vector(
            (antenna_1.x, antenna_1.y), (antenna_2.x, antenna_2.y)
        )
        self.x = antenna_1.x + x_vector
        self.y = antenna_1.y + y_vector

    def is_within_bounds(self, max_x, max_y):
        return self.x >= 0 and self.y >= 0 and self.x < max_x and self.y < max_y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Antinode({self.x}, {self.y})"


class Antenna:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Antenna({self.x}, {self.y})"


def vector(a, b):
    return (a[0] - b[0], a[1] - b[1])


def solution(input):
    antenna_positions = collections.defaultdict(collections.deque)
    _input = read_input(input)
    for col, line in enumerate(_input):
        for row, char in enumerate(line):
            if char != ".":
                antenna_positions[char].append((row, col))

    antinodes = set()
    max_y = len(_input)
    max_x = len(_input[0])
    for positions in antenna_positions.values():
        while len(positions) > 1:
            antenna = Antenna(*positions.popleft())
            for x_other, y_other in positions:
                other_antenna = Antenna(x_other, y_other)

                antinode_1 = Antinode(antenna, other_antenna)
                antinode_2 = Antinode(other_antenna, antenna)

                antinode_1.is_within_bounds(max_x, max_y) and antinodes.add(antinode_1)
                antinode_2.is_within_bounds(max_x, max_y) and antinodes.add(antinode_2)
    return len(antinodes)


assert solution("example.txt") == 14
print("solution: ", solution("input.txt"))
