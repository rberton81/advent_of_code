import collections
import os
from copy import deepcopy

from utils import Directions, Map

example_solution = 102
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]

class Map:
    def build_map(self, input):
        map = collections.defaultdict()

        y = 0
        for line in input:
            x = 0
            map[y] = collections.defaultdict()
            for char in line:
                # map[y][x] = {"heat": int(char), "path_heat": float("inf")}
                map[y][x] = int(char)
                x += 1
            y += 1

        return map

    def __init__(self, input):
        self.map = self.build_map(input)

    def print(self):
        print("___________________________")
        for x, tiles in self.map.items():
            # print(" ".join([str(tile["heat"]) for tile in tiles.values()]))
            print(" ".join([str(tile) for tile in tiles.values()]))
        return ""


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines

class Path:
    def __init__(self,x,y,heat, direction):
        self.x = x
        self.y = y
        self.heat = heat
        self.direction = direction

    def __repr__(self):
        return f"path {self.x, self.y}; heat: {self.heat}; direction: {self.direction}"


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def get_solution(input):
    city_map = Map(input)
    # city_map.print()
    heat_map = deepcopy(city_map)
    map = heat_map.map
    paths = collections.deque()
    leap_size = 3
    visited = set()
    min_heat = float('inf')

    current_total_heat = 0
    for x in range(1, leap_size+1):
        current_total_heat += city_map.map[0][0 + x]
        heat_map_cell = map[0][0 + x]
        if (0,x) not in visited or current_total_heat < heat_map_cell:
            heat_map_cell = current_total_heat
            paths.append(Path(x,0,current_total_heat, Directions.RIGHT))  
            visited.add((0,x))

    #DOWN
    current_total_heat = 0
    for y in range(1,leap_size+1):
        heat_map_cell = map[0+y][0]
        current_total_heat += city_map.map[0+y][0]
        if (y,0) not in visited or current_total_heat < heat_map_cell:
            heat_map_cell = current_total_heat  
            paths.append(Path(0,0+y,current_total_heat, Directions.DOWN))  
            visited.add((y,0))
    
    # assert len(paths) == 6
    # heat_map.print()

    while paths:
        path = paths.popleft()
        # print(f"{path}, current tile {city_map.map[path.y][path.x]}")
        # import pdb; pdb.set_trace()

        ##TODO compare path heat with current!

        # if path.heat < map[path.y][path.x]: ##TODO visited?
        if True: ##TODO visited?
            # map[path.y][path.x] = path.heat
            if path.x == len(map[0])-1 and path.y == len(map)-1:
                min_heat = min(min_heat, path.heat)
                print(f"min_heat: {min_heat}")
                import pdb; pdb.set_trace()
                print('foo')

            if path.direction in [Directions.RIGHT, Directions.LEFT]:
                current_heat_up = path.heat
                current_heat_down = path.heat
                
                for y in range(1,leap_size+1):
                    # print(f"y {y}")
                    try:
                        current_heat_down += city_map.map[path.y+y][path.x]
                        if (path.x, path.y+y) not in visited or current_heat_down < map[path.y+y][path.x]:
                            map[path.y+y][path.x] = current_heat_down
                            new_path = Path(path.x, path.y + y, current_heat_down, Directions.DOWN)
                            # print(f"1 added path {new_path}")
                            paths.append(new_path)
                            visited.add((path.x,path.y+y))
                    except KeyError:
                        pass
                    try:
                        current_heat_up += city_map.map[path.y-y][path.x]
                        if (path.x, path.y-y) not in visited or current_heat_up < map[path.y-y][path.x]:
                            map[path.y-y][path.x] = current_heat_up
                            new_path = Path(path.x, path.y - y, current_heat_up, Directions.UP)
                            # print(f"2 added path {new_path}")
                            paths.append(new_path)
                            visited.add((path.x,path.y-y))
                    except KeyError:
                        pass
                        
            elif path.direction in [Directions.UP, Directions.DOWN]:
                    current_heat_left = path.heat
                    current_heat_right = path.heat
                    for x in range(1,leap_size+1):
                        # print(f"x {x}")
                        try:
                            current_heat_left += city_map.map[path.y][path.x - x]
                            if (path.x-x, path.y) not in visited or current_heat_left < map[path.y][path.x - x]:
                                map[path.y][path.x - x] = current_heat_left
                                new_path = Path(path.x - x, path.y, current_heat_left, Directions.LEFT)
                                # print(f"3 added path {new_path}")
                                paths.append(new_path)
                                visited.add((path.x-x,path.y))
                        except KeyError:
                            pass
                        try:
                            current_heat_right += city_map.map[path.y][path.x + x]
                            if (path.x+x, path.y) not in visited or current_heat_right < map[path.y][path.x + x]:
                                map[path.y][path.x + x] = current_heat_left
                                new_path = Path(path.x+x, path.y, current_heat_right, Directions.RIGHT)
                                # print(f"4 added path {new_path}")
                                paths.append(new_path)
                                visited.add((path.x+x,path.y))
                        except KeyError:
                            pass
        # else:
        #     print(f"path {path} was inefficient!")
        # print('done with path')
        # heat_map.print()
        # city_map.print()
    # return heat_map.map[len(heat_map)][len(heat_map[0])]
    return min_heat




example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
assert solution < 1050
