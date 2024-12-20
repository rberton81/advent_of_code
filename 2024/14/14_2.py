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


def show_robots(robot_positions, map_dimensions):
    max_x, max_y = map_dimensions
    for x in range(max_x):
        for y in range(max_y):
            if (x, y) in robot_positions:
                print("#", end="")
            else:
                print(".", end="")
        print()


def solution(input, map_dimensions):
    max_x, max_y = map_dimensions
    period = 10403
    robots = []
    for line in read_input(input):
        robot = Robot(line)
        robots.append(robot)

    seconds = 0
    max_robots_in = 0
    while True:
        robot_positions = set()
        robots_out = 0
        for robot in robots:
            x_vel, y_vel = robot.velocity
            x_init, y_init = robot.position
            x_pos_after = (x_init + seconds * x_vel) % max_x
            y_pos_after = (y_init + seconds * y_vel) % max_y

            # Search when robots agglomerate near the center
            if (
                x_pos_after > 70
                or x_pos_after < 30
                or y_pos_after > 70
                or y_pos_after < 30
            ):
                robots_out += 1
            robots_in = len(robots) - robots_out
            robot_positions.add((x_pos_after, y_pos_after))

        if robots_in >= max_robots_in:
            max_robots_in = robots_in
            show_robots(robot_positions, map_dimensions)
            breakpoint()  # Is there a Christmas Tree?

        if seconds > period:
            break
        seconds += 1


_solution = solution("input.txt", (101, 103))
print("solution: ", _solution)
