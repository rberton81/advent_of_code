import collections
import os

example_solution = 46
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


class Map:
    def build_map(self, input):
        map = collections.defaultdict()

        y = 0
        for line in input:
            x = 0
            map[y] = collections.defaultdict()
            for char in line:
                map[y][x] = {"char": char, "is_energized": False}
                x += 1
            y += 1

        return map

    def __init__(self, input):
        self.map = self.build_map(input)

    def print(self):
        for x, tiles in self.map.items():
            print(" ".join([tile["char"] for tile in tiles.values()]))
        return ""


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


MIRRORS_TO_DIRECTION = {
    "\\": {"L": ["U"], "R": ["D"], "U": ["L"], "D": ["R"]},
    "|": {"L": ["U", "D"], "R": ["U", "D"], "U": ["U"], "D": ["D"]},
    "/": {"L": ["D"], "R": ["U"], "U": ["R"], "D": ["L"]},
    "-": {"L": ["L"], "R": ["R"], "U": ["L", "R"], "D": ["L", "R"]},
}


class Beam:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def __repr__(self):
        return f"position: {self.position}; direction: {self.direction}"

    def propagate(self, map):
        new_energized_tiles = 0
        current_x, current_y = self.position
        if not map[current_y][current_x]["is_energized"]:
            new_energized_tiles += 1
            map[current_y][current_x]["is_energized"] = True

        next_char = "."
        while next_char == ".":
            if self.direction == "R":
                current_x += 1
            elif self.direction == "L":
                current_x -= 1
            elif self.direction == "U":
                current_y -= 1
            elif self.direction == "D":
                current_y += 1
            try:
                next_char = map[current_y][current_x]["char"]
                if not map[current_y][current_x]["is_energized"]:
                    map[current_y][current_x]["is_energized"] = True
                    new_energized_tiles += 1
            except KeyError:
                return [], new_energized_tiles

        new_beam_directions = MIRRORS_TO_DIRECTION[next_char][self.direction]
        new_beams = [
            Beam((current_x, current_y), new_beam_direction)
            for new_beam_direction in new_beam_directions
        ]
        return new_beams, new_energized_tiles


def get_solution(input):
    mirror_map = Map(input)
    energized_tiles = 0
    propagated_beams = set()
    beams = collections.deque()
    initial_char = mirror_map.map[0][0]["char"]

    if initial_char != ".":
        for direction in MIRRORS_TO_DIRECTION[initial_char]["R"]:
            beams.append(Beam([0, 0], direction))
            propagated_beams.add(((0, 0), direction))
    else:
        beams.append(Beam([0, 0], "R"))

    while beams:
        beam = beams.popleft()
        new_beams, new_energized_tiles = beam.propagate(mirror_map.map)

        for new_beam in new_beams:
            beam_hash = (
                (new_beam.position[0], new_beam.position[1]),
                new_beam.direction,
            )
            if beam_hash not in propagated_beams:
                propagated_beams.add(beam_hash)
                beams.append(new_beam)

        energized_tiles += new_energized_tiles

    return energized_tiles


example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
