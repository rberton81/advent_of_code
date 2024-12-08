import collections
from utils.utils import read_input


class Antenna:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Antenna({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Antinode:
    @staticmethod
    def from_antennas(antenna_1: Antenna, antenna_2: Antenna, max_x, max_y):
        x_vector, y_vector = vector(
            (antenna_1.x, antenna_1.y), (antenna_2.x, antenna_2.y)
        )

        antinodes = set()
        offset = 0
        is_in_bounds_1 = True
        is_in_bounds_2 = True
        while True:
            if not is_in_bounds_1 and not is_in_bounds_2:
                break
            if is_in_bounds_1:
                antinode_1 = Antinode(
                    antenna_1.x + offset * x_vector, antenna_1.y + offset * y_vector
                )
                if not antinode_1.is_within_bounds(max_x, max_y):
                    is_in_bounds_1 = False
                else:
                    antinodes.add(antinode_1)
            if is_in_bounds_2:
                antinode_2 = Antinode(
                    antenna_2.x - offset * x_vector, antenna_2.y - offset * y_vector
                )
                if not antinode_2.is_within_bounds(max_x, max_y):
                    is_in_bounds_2 = False
                else:
                    antinodes.add(antinode_2)
            offset += 1
        return antinodes

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_within_bounds(self, max_x, max_y):
        return self.x >= 0 and self.y >= 0 and self.x < max_x and self.y < max_y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Antinode({self.x}, {self.y})"


def vector(a, b):
    return (a[0] - b[0], a[1] - b[1])


def solution(input):
    antenna_positions = collections.defaultdict(collections.deque)
    _input = read_input(input)
    for col, line in enumerate(_input):
        for row, char in enumerate(line):
            if char not in [".", "#"]:
                antenna_positions[char].append((row, col))

    antinodes = set()
    max_y = len(_input)
    max_x = len(_input[0])
    for _, positions in antenna_positions.items():
        while len(positions) > 1:
            antenna = Antenna(*positions.popleft())
            for x_other, y_other in positions:
                other_antenna = Antenna(x_other, y_other)
                antinodes.update(
                    Antinode.from_antennas(antenna, other_antenna, max_x, max_y)
                )
    return len(antinodes)


assert solution("example.txt") == 34
_solution = solution("input.txt")
print("solution: ", _solution)
