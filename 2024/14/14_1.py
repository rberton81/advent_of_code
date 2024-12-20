from collections import defaultdict
import math
from utils.utils import read_input


class Robot:
    def __init__(self, line):
        position, velocity = line.split()
        position = tuple([int(_) for _ in position.split("=")[1].split(",")])
        velocity = tuple([int(_) for _ in velocity.split("=")[1].split(",")])
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f"Robot(p={self.position}, v={self.velocity})"


def get_quadrants(x, y, x_mid, y_mid):
    if x < x_mid and y < y_mid:
        return 1
    elif x > x_mid and y < y_mid:
        return 2
    elif x < x_mid and y > y_mid:
        return 3
    elif x > x_mid and y > y_mid:
        return 4


def solution(input, map_dimensions):
    robots = []
    seconds = 100

    max_x, max_y = map_dimensions
    x_mid = max_x // 2
    y_mid = max_y // 2
    robot_count_by_quadrant = defaultdict(int)

    for line in read_input(input):
        robot = Robot(line)
        robots.append(robot)
        x_vel, y_vel = robot.velocity
        x_init, y_init = robot.position
        x_pos_after = (x_init + seconds * x_vel) % max_x
        y_pos_after = (y_init + seconds * y_vel) % max_y
        quadrant = get_quadrants(x_pos_after, y_pos_after, x_mid, y_mid)
        if quadrant:
            robot_count_by_quadrant[quadrant] += 1

    result = math.prod(robot_count_by_quadrant.values())
    return result


assert solution("example.txt", (11, 7)) == 12
_solution = solution("input.txt", (101, 103))
print("solution: ", _solution)
