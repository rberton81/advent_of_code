import collections
import math



class Directions:
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


STRING_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


STRING_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


class Tree:
    # Node = collections.namedtuple("Node", ["key", "paths"])

    # def __init__(self, strings): ##TODO with nodes
    #     # "one" to {"o": {"n": "e":{}}}
    #     self.tree = Tree.Node(key="root", paths=[])
    #     for string in strings:
    #         current_node = self.tree
    #         for char in string:
    #             if char in [node.key for node in current_node.paths]:
    #                 current_node = current_node.paths.find_key(char) #FIX
    #             else:
    #                 current_node[char] = Tree.Node(key="", paths=[])
    #             current_node = current_node[char]
    #             current_node[char] = current_node[char] if char in current_node else {}

    def build(self, strings):
        # "one" to {"o": {"n": "e":{}}}
        tree = {}
        for string in strings:
            current_node = tree
            for char in string:
                current_node[char] = current_node[char] if char in current_node else {}
                current_node = current_node[char]
        return tree

    def __init__(self, strings):
        self.tree = self.build(strings)
        self.max_lookup_distance = len(max(strings, key=len))
        self.reversed_tree = self.build([string[::-1] for string in strings])

    def list_is_in_tree_path(self, list, direction=Directions.RIGHT):
        current_node = self.tree
        path = []
        _list = list

        if direction == Directions.LEFT:
            current_node = self.reversed_tree

        for char in _list:
            try:
                current_node = current_node[char]
                path.append(char)
                if not current_node:
                    return path
            except KeyError:
                return False

        return False


class Map:
    def build_map(self, input):
        map = collections.defaultdict()

        y = 0
        for line in input:
            x = 0
            map[y] = collections.defaultdict()
            for char in line:
                map[y][x] = char
                x += 1
            y += 1

        return map

    def __init__(self, input):
        self.map = self.build_map(input)

    def print(self):
        for x, y__char in self.map.items():
            print(" ".join(y__char.values()))
        return ""


def lcm_of_list(numbers):
    lcm_result = 1
    for number in numbers:
        lcm_result = lcm_result * number // math.gcd(lcm_result, number)
    return lcm_result


def print_map(map):
    for y in range(len(map)):
        chars = [node["char"] for node in map[y].values()]
        print("".join(chars))


def get_lists_diff_count(list_1, list_2):
    diff_count = 0
    for elem_1, elem_2 in zip(list_1, list_2):
        if elem_1 != elem_2:
            diff_count += 1
    return diff_count

class DirectedGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex not in self.graph:
            self.graph[from_vertex] = []
        self.graph[from_vertex].append(to_vertex)

    def display(self):
        for vertex in self.graph:
            print(f"{vertex} -> {', '.join(map(str, self.graph[vertex]))}")

def get_middle_element(list):
    middle_index = len(list) // 2
    return list[middle_index]