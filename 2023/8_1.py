import collections
from utils import read_input
import re
import collections

example = read_input("8_example.txt")


def get_inputs(current__left__right):
    current, left__right = current__left__right.split("=")
    current = current.replace(" ", "")
    left, right = re.match(
        r"\(([A-Z]{3}),\s*([A-Z]{3})\)", left__right.replace(" ", "")
    ).group(1, 2)
    return current, left, right


def to_tree(input):
    Node = collections.namedtuple("Node", ["left", "right"])
    tree = collections.defaultdict(Node)

    for current__left__right in input:
        current, left, right = get_inputs(current__left__right)
        node = Node(left, right)
        tree[current] = node

    return tree


def get_solution(input):
    tree = to_tree(input[2:])
    instructions = collections.deque(input[0])
    current_instructions = instructions.copy()
    steps = 0

    next = "AAA"

    while next != "ZZZ":
        node = tree[next]

        if not current_instructions:
            current_instructions = instructions.copy()
        instruction = current_instructions.popleft()
        next = node.left if instruction == "L" else node.right
        steps += 1
    return steps


assert get_solution(example) == 2

input = read_input("./8_input.txt")
print("solution", get_solution(input))
