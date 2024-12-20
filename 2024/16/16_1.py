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
    return (x1 + x2, y1 + y2)


def turn(current_direction, rotation):
    directions = collections.deque(
        [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]
    )
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
        def __init__(self, pos, is_wall=False, is_end=False):
            self.is_wall = is_wall
            self.is_end = is_end
            self.pos = pos
            self.path_score = 0

        def __repr__(self):
            return f"{self.pos}"

        def is_current_best_path(self, previous_cell, score):
            return not self.is_wall and (
                not self.path_score
                or self.path_score > previous_cell.path_score + score
            )

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
                else:
                    if char == START:
                        reindeer = Reindeer((x, y), Directions.RIGHT)
                    map[y][x] = Map.Cell((x, y))
        return Map(map), reindeer

    def get(self, x, y) -> Cell:
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None

    def explore_cell(self, cell: Cell, direction):
        straight, left, right = get_straight__left__right(direction)
        next_paths = []

        cell_straight = self.get(*add(cell.pos, straight))
        if cell_straight.is_current_best_path(cell, 1):
            cell_straight.path_score = cell.path_score + 1
            next_paths.append((cell_straight, direction))

        cell_left = self.get(*add(cell.pos, left))
        if cell_left.is_current_best_path(cell, 1001):
            cell_left.path_score = cell.path_score + 1001
            next_paths.append((cell_left, turn(direction, SIDES.LEFT)))

        cell_right = self.get(*add(cell.pos, right))
        if cell_right.is_current_best_path(cell, 1001):
            cell_right.path_score = cell.path_score + 1001
            next_paths.append((cell_right, turn(direction, SIDES.RIGHT)))
        return next_paths


def solution(input):
    lowest_path_score = float("inf")
    map, reindeer = Map.build_map(read_input(input))

    start_cell = map.get(*reindeer.position)
    path_queue = collections.deque([(start_cell, reindeer.direction)])

    while path_queue:
        cell, direction = path_queue.pop()
        if cell.is_end:
            lowest_path_score = min(lowest_path_score, cell.path_score)
            continue
        next_paths = map.explore_cell(cell, direction)
        path_queue += next_paths

    return lowest_path_score


assert solution("example.txt") == 7036
assert solution("example_1.txt") == 11048
_solution = solution("input.txt")
print("solution: ", _solution)
