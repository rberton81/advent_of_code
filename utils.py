import collections
import math


class Directions:
    LEFT = "left"
    RIGHT = "right"


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

    def show_map(self):
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