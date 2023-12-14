import collections
from utils import read_input
from copy import deepcopy

right_enclosure_by_entry = {
    #entry_direction: enclosure, exit_direction
    "F": {
        "left": ([(0,-1), (-1,0), (-1,-1)],"down"),
        "up": ([(1,1)], "right"),
    },
    "|": {
        "down": ([(-1,0)], "down"),
        "up": ([(1,0)], "up")
    },
    "L": {
        "left": ([(1,-1)],"up"),
        "down": ([(-1,0), (0,1), (-1,1)], "right"),
    },
    "-": {
        "left": ([(0,-1)],"left"),
        "right": ([(0,1)], "right")
    },
    "J": {
        "right": ([(0,1), (1,0),(1,1)], "up"),
        "down": ([(-1,-1)], "left")
    },
    "7": {
        "right": ([(-1,1)], "down"),
        "up": ([(0,-1),(1,-1),(1,0)], "left")
    }
}

left_enclosure_by_entry = {
    #entry_direction: enclosure, exit_direction
    "F": {
        "left": ([(1,1)],"down"),
        "up": ([(0,-1), (-1,0), (-1,-1)], "right"),
    },
    "|": {
        "down": ([(1,0)], "down"),
        "up": ([(-1,0)], "up")
    },
    "L": {
        "left": ([(-1,0), (0,1), (-1,1)],"up"),
        "down": ([(1,-1)], "right"),
    },
    "-": {
        "left": ([(0,1)],"left"),
        "right": ([(0,-1)], "right")
    },
    "J": {
        "right": ([(-1,-1)], "up"),
        "down": ([(0,1), (1,0),(1,1)], "left")
    },
    "7": {
        "right": ([(0,-1),(1,-1),(1,0)], "down"),
        "up": ([(-1,1)], "left")
    }
}

def identify_start(x__y, map):
    x, y = x__y
    connections = []
    try:
        if map[y+1][x]["char"] in ["|", "F", "L"]:
            connections.append("D")
    except KeyError:
        pass
    try:
        if map[y][x-1]["char"] in ["-", "L", "F"]:
            connections.append("L")
    except KeyError:
        pass
    try:
        if map[y][x+1]["char"] in ["-", "7", "J"]:
            connections.append("R")
    except KeyError:
        pass
    try:
        if map[y-1][x]["char"] in ["|", "7", "J"]:
            connections.append("U")
    except KeyError:
        pass
    
    connections.sort()

    if connections == ["D", "R"]:
        return "F"
    elif connections == ["R", "U"]:
        return "L"
    elif connections == ["L", "R"]:
        return "-"
    elif connections == ["D", "U"]:
        return "|"
    elif connections == ["L", "U"]:
        return "J"
    elif connections == ["D", "L"]:
        return "7"
    
    
class Node:
    def __init__(self, x__y, map):
        self.x, self.y = list(x__y)
        self.char = map[self.y][self.x]['char']
        self.neighbors = []
        self.is_start = False

        if self.char == "S":
            self.char = identify_start(x__y, map)
            self.is_start = True

        x__ys = None
        if self.char == "F":
            x__ys = [(self.x+1, self.y), (self.x, self.y+1)]
        elif self.char == "|":
            x__ys = [(self.x, self.y-1), (self.x, self.y+1)]
        elif self.char == "L":
            x__ys = [(self.x, self.y-1), (self.x+1, self.y)]
        elif self.char == "-":
            x__ys = [(self.x-1, self.y), (self.x+1, self.y)]
        elif self.char == "J":
            x__ys = [(self.x-1, self.y), (self.x, self.y-1)]
        elif self.char == "7":
            x__ys = [(self.x-1, self.y), (self.x, self.y+1)]
        
        self.neighbors = x__ys


def to_graph(input):
    map = collections.defaultdict(collections.defaultdict)
    y = 0
    start__x__y = None
    enclosed_tiles = 0

    for line in input:
        x = 0
        for char in line:
            if char == "S":
                start__x__y = (x, y)
            map[y][x] = {
                "char": char,
                "is_loop": False,
            }
            enclosed_tiles += 1
            x += 1
        y += 1

    root = Node(start__x__y, map)
    return root, map, enclosed_tiles

def bfs(root, map, enclosed_tiles):
    visited = set()
    loop_nodes = set()

    queue = collections.deque([root])

    while queue:
        node = queue.popleft()
        if (node.x, node.y) not in visited:
            loop_nodes.add((node.x, node.y))
            map[node.y][node.x]["is_loop"] = True
            visited.add((node.x, node.y))

            for neighbor_x__y in node.neighbors:
                queue.append(Node(neighbor_x__y, map))
    
    return loop_nodes, map, enclosed_tiles


def get_solution(input):
    graph_root, map, enclosed_tiles = to_graph(input)
    start_x__y = (graph_root.x, graph_root.y)

    loop_nodes, map, enclosed_tiles = bfs(graph_root, map, enclosed_tiles)

    direction = "down"
    map_left = deepcopy(map)
    enclosed_tiles_left = 0
    map_right = deepcopy(map)
    enclosed_tiles_right = 0
    start_x, start_y = start_x__y
    current_x, current_y = None, None

    while current_x != start_x or current_y != start_y:
        if current_x is None and current_x is None:
            current_x, current_y = start_x__y

        if direction == "down":
            current_y += 1
        elif direction == "up":
            current_y -= 1
        elif direction == "left":
            current_x -= 1
        elif direction == "right":
            current_x += 1

        current_char = map[current_y][current_x]["char"]
        if current_char == "S":
            break

        ## RIGHT
        x_y_buffers, next_direction = right_enclosure_by_entry[current_char][direction]
        for x_buffer, y_buffer in x_y_buffers:
            try:
                enclosed_right = map_right[current_y+y_buffer][current_x+x_buffer]
                if not enclosed_right["is_loop"] and enclosed_right["char"] != "I":
                        enclosed_tiles_right += 1
                        enclosed_right["char"] = "I"
            except KeyError:
                pass

        ## LEFT
        x_y_buffers, next_direction = left_enclosure_by_entry[current_char][direction]
        for x_buffer, y_buffer in x_y_buffers:
            try:
                enclosed_left = map_left[current_y+y_buffer][current_x+x_buffer]
                if not enclosed_left["is_loop"] and enclosed_left["char"] != "I":
                        enclosed_tiles_left += 1
                        enclosed_left["char"] = "I"
            except KeyError:
                pass
            
        direction = next_direction
    
    ## FILL RIGHT
    for y, x__details in map_right.items():
        for x, details in x__details.items():
            for x_buffer, y_buffer in [(0,-1), (1,0), (0,1), (-1,0)]:
                node = map_right[y][x]
                if node["is_loop"] or node["char"] == "I":  
                    continue
                if y+y_buffer in map_right and x+x_buffer in map_right[y+y_buffer]:
                    neighbor = map_right[y+y_buffer][x+x_buffer]
                else:
                    continue
                if neighbor["char"] == "I":
                    node["char"] = "I"
                    enclosed_tiles_right += 1

    ## FILL LEFT
    for y, x__details in map_left.items():
        for x, details in x__details.items():
            if details["char"] == "I":
                for x, y in [(0,-1), (1,0), (0,1), (-1,0)]:
                    if y in map_left and x in map_left[y]:
                        neighbor = map_left[y][x]
                    else:
                        continue
                    if neighbor["is_loop"] or neighbor["char"] == "I":
                        continue
                    neighbor["char"] = "I"
                    enclosed_tiles_left += 1

    return min(enclosed_tiles_left, enclosed_tiles_right) # not always min but always one of these two.


example = read_input("10_2_example.txt")
assert (get_solution(example) == 10)

input = read_input("10_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
