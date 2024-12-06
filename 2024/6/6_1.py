import collections
from utils.utils import read_input

class MapChars:
    DOT = "."
    WALL = "#"

class GuardedMap:
    class MapCell:
        def __init__(self, pos, char, was_visited=False):
            self.was_visited = was_visited
            self.pos = pos
            self.char = char

    def build_map(self, input):
        map = collections.defaultdict()

        for y, line in enumerate(input):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char in [Guard.Directions.UP, Guard.Directions.DOWN, Guard.Directions.LEFT, Guard.Directions.RIGHT]:
                    guard = Guard((x, y), char)
                    map[y][x] = GuardedMap.MapCell((x, y), MapChars.DOT, was_visited=True)
                else:
                    map[y][x] = GuardedMap.MapCell((x, y), char)
        return map, guard

    def __init__(self, input):
        self.map, self.guard = self.build_map(input)

    def print(self):
        guard_pos = self.guard.position
        for y, x__cell in self.map.items():
            row = []
            for x, cell in x__cell.items():
                if (x, y) == guard_pos:
                    row.append(self.guard.direction)
                else:
                    row.append(cell.char)
            print(" ".join(row))
        return ""
    
    def get_char_in_front_of_guard(self):
        if self.guard.direction == Guard.Directions.UP:
            x, y = (self.guard.position[0], self.guard.position[1] - 1)
        elif self.guard.direction == Guard.Directions.DOWN:
            x, y = (self.guard.position[0], self.guard.position[1] + 1)
        elif self.guard.direction == Guard.Directions.LEFT:
            x, y = (self.guard.position[0] - 1, self.guard.position[1])
        elif self.guard.direction == Guard.Directions.RIGHT:
            x, y = (self.guard.position[0] + 1, self.guard.position[1])
        
        return self.map[y][x], (x, y)


    def move_guard(self):
        visited_cells = 1
        while True:
            try:
                cell, pos = self.get_char_in_front_of_guard()
                if cell.char == MapChars.WALL:
                    self.guard.turn_right()
                else:
                    if not cell.was_visited:
                        cell.was_visited = True
                        visited_cells += 1
                    self.guard.go_to(pos)
            except KeyError:
                break
            
        return visited_cells

class Guard:
    class Directions:
        UP = "^"
        RIGHT = ">"
        DOWN = "v"
        LEFT = "<"

        CLOCKWISE = collections.deque([UP, RIGHT, DOWN, LEFT])

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def go_to(self, position):
        self.position = position

    def turn_right(self):
        new_direction_idx = (Guard.Directions.CLOCKWISE.index(self.direction) + 1) % len(Guard.Directions.CLOCKWISE)
        self.direction = Guard.Directions.CLOCKWISE[new_direction_idx]
    
def solution(input):
    map = GuardedMap(read_input(input))
    visited_cells = map.move_guard()
    return visited_cells

assert solution("example.txt") == 41
print("solution: ", solution("input.txt"))
