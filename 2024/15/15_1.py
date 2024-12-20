import collections
from utils.utils import read_input

WALL = "#"
CRATE = "O"
ROBOT = "@"
EMPTY_SPACE = "."


class Directions:
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


class Robot:
    def __init__(self, position):
        self.position = position


class Map:
    def __init__(self, map):
        self.map = map

    class Cell:
        def __init__(self, pos, is_wall=False, is_crate=False):
            self.is_wall = is_wall
            self.is_crate = is_crate
            self.pos = pos

    @staticmethod
    def build_map(lines):
        map = collections.defaultdict()
        robot = None
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char == WALL:
                    map[y][x] = Map.Cell((x, y), is_wall=True)
                elif char == CRATE:
                    map[y][x] = Map.Cell((x, y), is_crate=True)
                else:
                    map[y][x] = Map.Cell((x, y))
                if char == ROBOT:
                    robot = Robot((x, y))
                    map[y][x] = Map.Cell((x, y))
        return Map(map), robot

    def get(self, x, y) -> Cell:
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None

    def get_next_empty_space(self, pos, direction) -> Cell:
        x, y = pos
        if direction == Directions.UP:
            pos_other = (x, y - 1)
        elif direction == Directions.RIGHT:
            pos_other = (x + 1, y)
        elif direction == Directions.DOWN:
            pos_other = (x, y + 1)
        elif direction == Directions.LEFT:
            pos_other = (x - 1, y)

        object = self.get(*pos_other)
        if object.is_wall:
            return None
        elif object.is_crate:
            return self.get_next_empty_space(pos_other, direction)
        else:
            return object

    def get_score(self):
        score = 0
        for y, x__cell in self.map.items():
            for x, cell in x__cell.items():
                if cell.is_crate:
                    score += y * 100 + x
        return score


def solution(input):
    map_rows = []
    directions = ""
    is_direction = False
    for line in read_input(input):
        if not line and not is_direction:
            is_direction = True
            continue

        if not is_direction:
            map_rows.append(line)
        else:
            directions += line

    map, robot = Map.build_map(map_rows)
    map.print(robot.position)

    for direction in directions:
        x, y = robot.position
        if direction == Directions.UP:
            pos_other = (x, y - 1)
        elif direction == Directions.RIGHT:
            pos_other = (x + 1, y)
        elif direction == Directions.DOWN:
            pos_other = (x, y + 1)
        elif direction == Directions.LEFT:
            pos_other = (x - 1, y)

        object = map.get(*pos_other)
        if object.is_wall:
            continue
        elif object.is_crate:
            next_empty_space = map.get_next_empty_space(pos_other, direction)
            if next_empty_space:
                object.is_crate = False
                robot.position = pos_other
                next_empty_space.is_crate = True
        else:
            robot.position = pos_other
    return map.get_score()


# assert solution("example_1.txt") == 2028
# assert solution("example.txt") == 10092
_solution = solution("input.txt")
print("solution: ", _solution)
