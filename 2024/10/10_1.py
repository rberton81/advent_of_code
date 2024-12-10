import collections
import itertools
from utils.utils import read_input

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

    topping_trailheads = 0
    for x_start, y_start in map.zeroes:
        trail = Trail((x_start, y_start), 0)
        trails = collections.deque([trail])
        topped_trailheads = set()
            
        while trails:
            trail = trails.popleft()
            x, y = trail.position
            
            for x_offset, y_offset in [(0,1), (0,-1), (1,0), (-1,0)]:
                try:
                    trail_cell: Map.Cell = map.map[y + y_offset][x + x_offset]
                    elevation = int(trail_cell.char)
                    if trail.elevation == 8 and elevation == 9:
                        if trail_cell.pos not in topped_trailheads:
                            topped_trailheads.add(trail_cell.pos)
                            topping_trailheads += 1
                    elif elevation == trail.elevation + 1:
                        trails.append(Trail((x + x_offset, y + y_offset), elevation))
                except KeyError:
                    continue
    return topping_trailheads
    
assert solution("example.txt") == 36
print("solution: ", solution("input.txt"))
