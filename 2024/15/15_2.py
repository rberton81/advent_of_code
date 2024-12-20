import collections
from utils.utils import read_input

WALL = "#"
CRATE = "O"
LEFT_CRATE = "["
RIGHT_CRATE = "]"
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
        def __init__(
            self, pos, is_wall=False, is_left_crate=False, is_right_crate=False
        ):
            self.is_wall = is_wall
            self.is_left_crate = is_left_crate
            self.is_right_crate = is_right_crate
            self.pos = pos

        def __repr__(self):
            return f"{self.pos}"

        def is_crate(self):
            return self.is_left_crate or self.is_right_crate

    @staticmethod
    def build_map(lines):
        map = collections.defaultdict()
        robot = None
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            x = 0
            for char in line:
                print(f"char: {char}")
                if char == WALL:
                    map[y][x] = Map.Cell((x, y), is_wall=True)
                    map[y][x + 1] = Map.Cell((x, y), is_wall=True)
                elif char == CRATE:
                    map[y][x] = Map.Cell((x, y), is_left_crate=True)
                    map[y][x + 1] = Map.Cell((x, y), is_right_crate=True)
                else:
                    if char == ROBOT:
                        robot = Robot((x, y))
                    map[y][x] = Map.Cell((x, y))
                    map[y][x + 1] = Map.Cell((x, y))
                x += 2
        return Map(map), robot

    def print(self, robot_pos):
        for y, x__cell in self.map.items():
            row = []
            for x, cell in x__cell.items():
                if (x, y) == robot_pos:
                    row.append(ROBOT)
                else:
                    if cell.is_wall:
                        row.append(WALL)
                    elif cell.is_left_crate:
                        row.append(LEFT_CRATE)
                    elif cell.is_right_crate:
                        row.append(RIGHT_CRATE)
                    else:
                        row.append(EMPTY_SPACE)
            print(" ".join(row))
        return ""

    def get(self, x, y) -> Cell:
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None

    def get_next_empty_space(self, pos, direction) -> Cell:
        print(f"trying to push {pos} in direction {direction}")
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
        print(f"object to push: {object}")
        if object.is_wall:
            return None
        elif object.is_crate():
            return self.get_next_empty_space(pos_other, direction)
        else:
            return object

    def get_score(self):
        score = 0
        for y, x__cell in self.map.items():
            for x, cell in x__cell.items():
                if cell.is_right_crate:
                    score += y * 100 + x
        return score

    def push_horizontally(self, x_vector, pos_other, next_empty_space):
        for idx in range(0, x_vector, -1) if x_vector < 0 else range(0, x_vector):
            print(f"idx: {idx}")
            crate = self.get(pos_other[0] + idx, pos_other[1])
            crate.is_left_crate, crate.is_right_crate = (
                crate.is_right_crate,
                crate.is_left_crate,
            )

        next_empty_space.is_left_crate = True if x_vector < 0 else False
        next_empty_space.is_right_crate = True if x_vector > 0 else False

    def push_vertically(self, init_pos, direction):
        crate = self.get(*init_pos)
        if direction == Directions.UP:
            other_pos = (init_pos[0], init_pos[1] - 1)
        elif direction == Directions.DOWN:
            other_pos = (init_pos[0], init_pos[1] + 1)

        other_object = self.get(*other_pos)

        if (crate.is_left_crate and other_object.is_left_crate) or (
            crate.is_right_crate and other_object.is_right_crate
        ):
            # straight push
            pass
        elif other_object.is_crate():
            # scramble push
            pass
        else:
            # is empty space, ok to push
            pass


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
        print(f"looking at direction: {direction}")
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
        elif object.is_crate():
            if direction in [Directions.LEFT, Directions.RIGHT]:
                next_empty_space = map.get_next_empty_space(pos_other, direction)
                if next_empty_space:
                    print(f"push to {next_empty_space}")
                    robot.position = object.pos
                    object.is_left_crate, object.is_right_crate = False, False
                    deplacement = next_empty_space.pos[0] - object.pos[0]
                    map.push_horizontally(deplacement, pos_other, next_empty_space)
                else:  # cannot push
                    print("cannot push")
            else:
                if object.is_left_crate:
                    left, right = object.pos, (object.pos[0] + 1, object.pos[1])
                else:
                    left, right = (object.pos[0] - 1, object.pos[1]), object.pos

                map.push_vertically(left, direction)
                map.push_vertically(right, direction)

        else:
            robot.position = pos_other

        map.print(robot.position)
        print(f"looking at  objects : {object}")
        import pdb

        pdb.set_trace()
        print("foo")

    score = map.get_score()
    print(f"score: {score}")
    return score


assert solution("example.txt") == 10092
_solution = solution("input.txt")
print("solution: ", _solution)
