import collections
from utils.utils import read_input

class MapChars:
    DOT = "."
    WALL = "#"
    VISITED_CELL = "X"

class GuardedMap: 
    def __init__(self, input=None, map=None, guard=None):
        if input:
            self.map, self.guard = self.build_map(input)
        else:
            self.map = map
            self.guard = guard

    class Cell:
        def __init__(self, pos, char, was_visited=False):
            self.was_visited = was_visited
            self.was_tried = False
            self.pos = pos
            self.char = char
        
        def __repr__(self):
            return f"{self.pos} -> {self.char}"

    def serialize(self):
        return {
            "map": self.map,
        }

    @classmethod
    def from_serialized(cls, map):
        instance = cls(map=map['map'])
        return instance

    def build_map(self, input):
        map = collections.defaultdict()

        for y, line in enumerate(input):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char in [Guard.Directions.UP, Guard.Directions.DOWN, Guard.Directions.LEFT, Guard.Directions.RIGHT]:
                    guard = Guard((x, y), char)
                    map[y][x] = GuardedMap.Cell((x, y), MapChars.DOT, was_visited=True)
                else:
                    map[y][x] = GuardedMap.Cell((x, y), char)
        return map, guard

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
    
    def get_cell_in_front_of_guard(self):
        x_guard, y_guard = self.guard.position
        if self.guard.direction == Guard.Directions.UP:
            x, y = (x_guard, y_guard - 1)
        elif self.guard.direction == Guard.Directions.DOWN:
            x, y = (x_guard, y_guard + 1)
        elif self.guard.direction == Guard.Directions.LEFT:
            x, y = (x_guard - 1, y_guard)
        elif self.guard.direction == Guard.Directions.RIGHT:
            x, y = (x_guard + 1, y_guard)
        return self.map[y][x]
    
    def move_guard(self):
        while True:
            try:
                cell = self.get_cell_in_front_of_guard()
                if cell.char == MapChars.WALL:
                    self.guard.turn_right()
                else:
                    if not cell.was_tried:
                        yield (self.guard.position, self.guard.direction)
                        cell.was_tried = True
                    self.guard.go_to(cell.pos)
                    cell.was_visited = True
            except KeyError:
                break
    
    def loops(self):
        start_direction = self.guard.direction
        visited_positions = set(self.guard.position)
        direction_by_visited_position = {self.guard.position: start_direction}
        start_cell = self.get_cell_in_front_of_guard()
        start_cell.char = MapChars.WALL

        block_loops = False
        while True:
            try:
                cell = self.get_cell_in_front_of_guard()
                if cell.char == MapChars.WALL:
                    self.guard.turn_right()
                else:
                    self.guard.go_to(cell.pos)
                    if self.guard.position in direction_by_visited_position.keys() and self.guard.direction == direction_by_visited_position[self.guard.position]:
                        block_loops = True
                        break
                    visited_positions.add(cell.pos)
                    direction_by_visited_position[cell.pos]= self.guard.direction
            except KeyError:
                break # out of map
        
        start_cell.char = MapChars.DOT
        return block_loops

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
        current_direction_idx = Guard.Directions.CLOCKWISE.index(self.direction)
        new_direction_idx = (current_direction_idx + 1) % len(Guard.Directions.CLOCKWISE)
        self.direction = Guard.Directions.CLOCKWISE[new_direction_idx]

    def turn_left(self):
        current_direction_idx = Guard.Directions.CLOCKWISE.index(self.direction)
        directions_length = len(Guard.Directions.CLOCKWISE)
        new_direction_idx = (directions_length + current_direction_idx - 1) % directions_length
        self.direction = Guard.Directions.CLOCKWISE[new_direction_idx]
    

def block_is_loop(serialized_map, guard_pos, guard_dir):
    map = GuardedMap.from_serialized(serialized_map)
    map.guard = Guard(guard_pos, guard_dir)
    if map.loops():
        return 1
    return 0

def solution(input):
    map = GuardedMap(read_input(input))
    map_init = map.serialize()
    
    loop_blocks = 0
    for guard_pos, guard_dir in map.move_guard():
        loop_blocks += block_is_loop(map_init, guard_pos, guard_dir)
  
    return loop_blocks

assert solution("example.txt") == 6
print("solution: ", solution("input.txt"))
