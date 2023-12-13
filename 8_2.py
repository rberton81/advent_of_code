import collections
from utils import lcm_of_list, read_input
import re
import collections

Node = collections.namedtuple("Node", ["left", "right"])


def get_inputs(current__left__right):
    current, left__right = current__left__right.split("=")
    current = current.replace(" ", "")
    left, right = re.match(
        r"\(([A-Z1-9]{3}),\s*([A-Z1-9]{3})\)", left__right.replace(" ", "")
    ).group(1, 2)
    return current, left, right


def gather_all_starts(input):
    paths = collections.defaultdict(collections.defaultdict)
    nodes_by_start = collections.defaultdict(set)  # {start: [values]}
    input_without_starts = []

    for current__left__right in input:
        current, left, right = get_inputs(current__left__right)

        if current[2] == "A":  # new path
            node = Node(left, right)
            paths[current] = collections.defaultdict(Node)
            paths[current][current] = node
            nodes_by_start[current] |= set([left, right])
        else:
            input_without_starts.append(current__left__right)

    return paths, nodes_by_start, input_without_starts


def extract_nodes_by_start(paths, nodes_by_start, input_without_starts, ends_by_start):
    input_leftovers = []

    for current__left__right in input_without_starts:
        current, left, right = get_inputs(current__left__right)

        added = False
        for start, nodes in nodes_by_start.items():
            if current in nodes and not added:
                node = Node(left, right)
                added = True
                paths[start][current] = node
                nodes_by_start[start] |= set([left, right])
                if current[2] == "Z":
                    ends_by_start[start] = current
                    ends_by_start["last_seen"] = current

        if not added:
            input_leftovers.append(current__left__right)

    return paths, nodes_by_start, input_leftovers, ends_by_start


def check_all_nodes_end_with_z(nodes):
    for node in nodes.values():
        if node[2] != "Z":
            return False
    return True


def get_solution(input):
    paths, nodes_by_start, input_without_starts = gather_all_starts(input[2:])
    ends_by_start = collections.defaultdict(str)

    while input_without_starts:
        (
            paths,
            nodes_by_start,
            input_without_starts,
            ends_by_start,
        ) = extract_nodes_by_start(
            paths, nodes_by_start, input_without_starts, ends_by_start
        )

    instructions = collections.deque(input[0])
    current_instructions = instructions.copy()
    steps = 0

    nexts = {start: start for start in paths.keys()}
    seen_ends = collections.defaultdict()
    buffer_to_complete_last_end = None

    class LoopEnd:
        def __init__(self, total_steps, current_steps):
            self.total_steps = total_steps
            self.current_steps = current_steps

    while True:
        if not current_instructions:
            current_instructions = instructions.copy()
        instruction = current_instructions.popleft()

        for end in seen_ends.values():
            end.current_steps += 1
            if end.current_steps > end.total_steps:
                end.total_steps = end.current_steps

        for start, nodes in paths.items():
            next = nexts[start]
            node = nodes[next]

            if next in ends_by_start.values():
                if next in seen_ends:
                    seen_ends[next].current_steps = 0
                else:
                    seen_ends[next] = LoopEnd(0, 0)
            nexts[start] = node.left if instruction == "L" else node.right

        steps += 1
        if len(ends_by_start) - 1 == len(seen_ends):
            if buffer_to_complete_last_end is None:
                buffer_to_complete_last_end = 2 * steps  # a tad random
            elif buffer_to_complete_last_end:
                buffer_to_complete_last_end -= 1
            elif buffer_to_complete_last_end == 0:
                lcm = lcm_of_list([loop.total_steps for loop in seen_ends.values()])
                return lcm


example = read_input("8_2_example.txt")
assert get_solution(example) == 6

input = read_input("./8_input.txt")
print("solution", get_solution(input))
