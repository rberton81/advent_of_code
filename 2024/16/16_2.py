import collections
from utils.utils import read_input

START = "S"
END = "E"
WALL = "#"
EMPTY_SPACE = "."


def get_straight__left__right(direction):
    if direction == Directions.UP:
        straight, left, right = (0, -1), (-1, 0), (1, 0)
    elif direction == Directions.RIGHT:
        straight, left, right = (1, 0), (0, -1), (0, 1)
    elif direction == Directions.DOWN:
        straight, left, right = (0, 1), (1, 0), (-1, 0)
    elif direction == Directions.LEFT:
        straight, left, right = (-1, 0), (0, 1), (0, -1)
    return straight, left, right
    
def add(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1+x2, y1+y2)


def turn(current_direction, rotation):
    directions = collections.deque([Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT])
    if rotation == SIDES.LEFT:
        new_idx = (directions.index(current_direction) - 1 + 4) % 4
    else:
        new_idx = (directions.index(current_direction) + 1) % 4
    return directions[new_idx]

class Directions:
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

class SIDES:
    LEFT = "L"
    RIGHT = "R"
    
class Reindeer:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class Map:
    def __init__(self, map):
        self.map = map

    class Cell:
        def __init__(self, pos, is_wall=False, is_end=False, is_start=False):
            self.is_wall = is_wall
            self.is_end = is_end
            self.is_start = is_start
            self.pos = pos
            self.path_score = 0
            self.was_counted = False

        def __repr__(self):
            return f"{self.pos}"
        
        def is_current_best_path(self, previous_cell, score):
            return not self.is_wall and (not self.path_score or self.path_score >= previous_cell.path_score + score)
        
    @staticmethod
    def build_map(lines):
        map = collections.defaultdict()
        reindeer = None
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char == WALL:
                    map[y][x] = Map.Cell((x, y), is_wall=True)
                elif char == END:
                    map[y][x] = Map.Cell((x, y), is_end=True)
                elif char == START:
                    reindeer = Reindeer((x, y), Directions.RIGHT)
                    map[y][x] = Map.Cell((x, y), is_start=True)
                else:
                    map[y][x] = Map.Cell((x, y))
        return Map(map), reindeer
    
    def get(self, x, y) -> Cell:
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None
        

    def explore_cell(self, cell:Cell, direction):
        straight, left, right = get_straight__left__right(direction)
        next_paths = []

        ##TODO path score needs to depend on direction for each cell!
        cell_straight = self.get(*add(cell.pos, straight))
        if cell_straight.is_current_best_path(cell, 1):
            cell_straight.path_score = cell.path_score + 1
            next_paths.append((cell_straight, direction))

        cell_left = self.get(*add(cell.pos, left))
        if cell_left.is_current_best_path(cell, 1001):
            cell_left.path_score = cell.path_score + 1001
            next_paths.append((cell_left, turn(direction, SIDES.LEFT)))

        cell_right = self.get(*add(cell.pos,  right))
        if cell_right.is_current_best_path(cell, 1001):
            cell_right.path_score = cell.path_score + 1001
            next_paths.append((cell_right, turn(direction, SIDES.RIGHT)))

        return next_paths
    
    def find_best_paths(self, cell):
        x, y = cell.pos
        current_lowest_score = float('inf')
        others: list[Map.Cell] = []
        
        for offset in (-1, 1):
            other_h = self.get(x + offset, y)
            other_v = self.get(x, y + offset)
            others += [other_h, other_v]

        for other in others:
            print(f"other: {other}, score={other.path_score}")
            if not other.is_wall and other.path_score and other.path_score <= current_lowest_score:
                if not other.was_counted:
                    other.was_counted = True
                    current_lowest_score = other.path_score

        next_paths = [other for other in others if other.path_score == current_lowest_score]
        print(f"Next is {next_paths}")
        return next_paths

    def follow_best_path_and_count_seats(self, end):
        tiles_count = 0
        next_paths = collections.deque([end])
        while next_paths:
            next_path = next_paths.popleft()
            _next_paths = self.find_best_paths(next_path)
            next_paths += _next_paths
            tiles_count += len(_next_paths)
            print(f"Looking at {next_path}, tiles_count={tiles_count}")
            import pdb; pdb.set_trace()
            if next_path.is_start:
                break
        return tiles_count

def solution(input):
    lowest_path_score = float('inf')
    map, reindeer = Map.build_map(read_input(input))

    start_cell = map.get(*reindeer.position)
    path_queue = collections.deque([(start_cell, reindeer.direction)])
    end_cell = None

    while path_queue:
        cell, direction = path_queue.pop()
        if cell.is_end:
            end_cell = cell
            lowest_path_score = min(lowest_path_score, cell.path_score)
            continue
        next_paths= map.explore_cell(cell, direction)
        print(f"next_paths: {next_paths}")
        path_queue += next_paths

    print('done settings scores')
    import pdb; pdb.set_trace()    
    seat_count = map.follow_best_path_and_count_seats(end_cell)
    print(f"seat count: {seat_count}")
    return lowest_path_score

assert solution("example.txt") == 45
assert solution("example_1.txt") == 64
# _solution = solution("input.txt")
# print("solution: ", _solution)
