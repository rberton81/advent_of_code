import collections
from utils import read_input

# F -> DR
# L -> RU
# - -> LR
# | -> DU
# J -> LU
# 7 -> DL

def identify_start(x__y, map):
    x, y = x__y
    connections = []
    try:
        if map[y+1][x] in ["|", "F", "L"]:
            connections.append("D")
    except KeyError:
        pass
    try:
        if map[y][x-1] in ["-", "L", "F"]:
            connections.append("L")
    except KeyError:
        pass
    try:
        if map[y][x+1] in ["-", "7", "J"]:
            connections.append("R")
    except KeyError:
        pass
    try:
        if map[y-1][x] in ["|", "7", "J"]:
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
        self.x, self.y = x__y
        self.char = map[self.y][self.x]
        self.neighbors = []

        if self.char == "S":
            self.char = identify_start(x__y, map)

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

    for line in input:
        x = 0
        for char in line:
            if char == "S":
                start__x__y = (x, y)
            map[y][x] = char
            x += 1
        y += 1

    root = Node(start__x__y, map)
    return root, map

def bfs(root, map):
    visited = set()
    queue = collections.deque([(root, 0)])
    max_distance = 0

    while queue:
        node, distance = queue.popleft()
        if (node.x, node.y) not in visited:
            max_distance = max(max_distance, distance)
            visited.add((node.x, node.y))
            for neighbor_x__y in node.neighbors:
                queue.append((Node(neighbor_x__y, map), distance+1))
    
    return max_distance

def get_solution(input):
    graph_root, map = to_graph(input)
    max_distance = bfs(graph_root, map)
    return max_distance

example = read_input("10_example.txt")
assert (get_solution(example) == 8)

input = read_input("10_input.txt")
print("solution", get_solution(input))