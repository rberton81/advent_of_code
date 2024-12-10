import collections
from utils.utils import read_input

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Map:
    def __init__(self, lines):
        self.map, self.zeroes = self.build_map(lines)

    class Cell:
        def __init__(self, pos, char, was_visited=False):
            self.was_visited = was_visited
            self.pos = pos
            self.char = char

        def __repr__(self):
            return f"{self.pos} -> {self.char}"

    def build_map(self, lines):
        map = collections.defaultdict()
        zeroes = set()
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char == "0":
                    zeroes.add((x, y))
                map[y][x] = Map.Cell((x, y), char)
        return map, zeroes
    
    def print(self):
        for y, x__cell in self.map.items():
            row = []
            for x, cell in x__cell.items():
                row.append(cell.char)
            print(" ".join(row))
        return ""

class Trail:
    def __init__(self, position, elevation):
        self.position = position
        self.elevation = elevation

    def __repr__(self):
        return f"Trail({self.position} -> {self.elevation})"


def solution(input):
    map = Map(read_input(input))    
    map.print()

    total_rating = 0
    for x_start, y_start in map.zeroes:
        trail = Trail((x_start, y_start), 0)
        trails = collections.deque([trail])
        trail_rating = 1

        while trails:
            trail = trails.popleft()
            x, y = trail.position
            trail_continues = False
            for x_offset, y_offset in [UP, DOWN, LEFT, RIGHT]:
                try:
                    trail_cell: Map.Cell = map.map[y + y_offset][x + x_offset]
                    try:
                        elevation = int(trail_cell.char)
                    except ValueError:
                        continue
                    
                    if trail.elevation == 8 and elevation == 9:
                        if trail_continues:
                            trail_rating += 1
                        trail_continues = True
                    elif elevation == trail.elevation + 1:
                        trails.append(Trail((x + x_offset, y + y_offset), elevation))
                        if trail_continues:
                            trail_rating += 1
                        trail_continues = True
                except KeyError:
                    continue
            if not trail_continues:
                trail_rating -= 1
        total_rating += trail_rating
    return total_rating
    
assert solution("example_1.txt") == 3
assert solution("example_2.txt") == 13
assert solution("example_3.txt") == 227
assert solution("example.txt") == 81
print("solution: ", solution("input.txt"))
