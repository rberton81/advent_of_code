import collections
import os
import math

from utils import get_lists_diff_count

example_solution = 400
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def validate_reflection(start, map, direction, can_be_fixed=False):
    print("validating, can be fixed: ", can_be_fixed, direction, start)
    # import pdb; pdb.set_trace()

    i = 1 if can_be_fixed else 0
    max_count = 0

    if start == 1:
        return can_be_fixed
    if direction == "V" and start == len(map[0]):
        return can_be_fixed
    if direction == "H" and start == len(map):
        return can_be_fixed

    if direction == "H":
        while True and max_count < 1000:
            try:
                print(f"checking {map[start+i]} and {map[start-i-1]}     -- 1 --")
                diff_count = get_lists_diff_count(map[start + i], map[start - i - 1])
                if diff_count == 1:
                    if can_be_fixed:
                        print("nope")
                        return False
                    can_be_fixed = True
            except IndexError:
                if can_be_fixed:
                    print(f"{start} can be fixed")
                else:
                    print(f"{start} is reflection but osef 3!")
                return can_be_fixed
            i += 1
            if start - i - 1 < 0:
                if can_be_fixed:
                    print("found it!")
                    return True
                print(f"{start} is reflection but osef 2!")
                return False
            max_count += 1
    elif direction == "V":
        print("test")
        while True and max_count < 1000:
            print("hellolol")
            try:
                for y in range(len(map)):
                    print(f"checking {map[y][start+i]} and {map[y][start-i-1]} -- 2 --")
                    if map[y][start + i] != map[y][start - i - 1]:
                        if can_be_fixed:
                            print("nope too")
                            return False
                        can_be_fixed = True
            except IndexError:
                if can_be_fixed:
                    print(f"{start} can be fixed")
                else:
                    print(f"{start} is reflection but osef 3!")
                return can_be_fixed
            i += 1
            if start - i - 1 < 0:
                if can_be_fixed:
                    print("found it!")
                    return True
                print(f"{start} is reflection but osef 4!")
                return False
            max_count += 1

        print("foo2?")
        import pdb

        pdb.set_trace()
        # return can_be_fixed ##TODO sure?
        print("foo")


def scan_horizontally(map):
    print("scanning horizontally")
    if len(map) % 2 == 0:
        up, down = len(map) - 2, len(map) - 1
        print(f"up {up} down {down}")
        diff_count = get_lists_diff_count(map[up], map[down])
        if diff_count <= 1:
            print("init found candidate reflection horizontally", up)
            if validate_reflection(up + 1, map, "H", can_be_fixed=diff_count == 1):
                return up * 100
    else:
        up, down = math.floor(len(map) / 2), math.ceil(len(map) / 2)

    while True:
        print(f"up {up} down {down}")
        if up >= 0:
            print(f"up -> comparing {map[up]} and {map[up+1]}")
        if down < len(map):
            print(f"down -> comparing {map[down]} and {map[down-1]}")
        # if up >= 0 and map[up] == map[up+1]:
        if up >= 0:
            up_diff_count = get_lists_diff_count(map[up], map[up + 1])
            if up_diff_count <= 1:
                print("up found candidate reflection horizontally", up)
                if validate_reflection(
                    up + 1, map, "H", can_be_fixed=up_diff_count == 1
                ):
                    return (up + 1) * 100
        # if down < len(map) and map[down] == map[down-1]:
        if down < len(map):
            down_diff_count = get_lists_diff_count(map[down], map[down - 1])
            if down_diff_count <= 1:
                print("down found candidate reflection horizontally", down)
                if validate_reflection(
                    down, map, "H", can_be_fixed=down_diff_count == 1
                ):
                    return down * 100

        up -= 1
        down += 1

        if up < 0 and down >= len(map):
            return None


def scan_vertically(map):
    print("scanning vertically")

    if len(map[0]) % 2 == 0:
        print("weird stuff lol")
        import pdb

        pdb.set_trace()
        pass
        # left, right = len(map[0]) - 2, len(map[0]) - 1
        # print(f"up {left} down {right}")
        # if map[left] == map[right]:
        #     print('init found candidate reflection vertically', left)
        #     if validate_reflection(left, map, "H"):
        #         return left ##TODO this shit broken!
    else:
        left, right = math.floor(len(map[0]) / 2), math.ceil(len(map[0]) / 2)

    while True:
        print(f"left {left} right {right}")

        left_is_reflection = True
        left_can_be_fixed = False
        right_is_reflection = True
        right_can_be_fixed = False

        for y in range(len(map)):
            if left >= 0:
                print(f"left -> comparing {map[y][left]} and {map[y][left+1]}")
            if right < len(map[0]):
                print(f"right -> comparing {map[y][right]} and {map[y][right-1]}")

            if left >= 0 and map[y][left] != map[y][left + 1]:
                # print('left not same!')
                if left_can_be_fixed:
                    print("left cant be fixed")
                    left_can_be_fixed = False
                if left_is_reflection:
                    left_can_be_fixed = True
                    left_is_reflection = False

            if right < len(map[0]) and map[y][right] != map[y][right - 1]:
                if right_can_be_fixed:
                    print("right cant be fixed")
                    right_can_be_fixed = False
                if right_is_reflection:
                    right_can_be_fixed = True
                    right_is_reflection = False

            if (
                not left_is_reflection
                and not left_can_be_fixed
                and not right_is_reflection
                and not right_can_be_fixed
            ):
                break

        # import pdb; pdb.set_trace()

        if left_is_reflection or left_can_be_fixed:
            print("left found candidate reflection vertically", left)
            if validate_reflection(left + 1, map, "V", can_be_fixed=left_can_be_fixed):
                return left + 1
            print("left cant be fixed")

        if right_is_reflection or right_can_be_fixed:
            print(
                "right found candidate reflection vertically", right
            )  ##TODO might be sometjing wrong here?
            if validate_reflection(right, map, "V", can_be_fixed=right_can_be_fixed):
                return right
            print("right cant be fixed")

        left -= 1
        right += 1

        if left < 0 and right >= len(map[0]):
            return None

    print("no vertical reflection")
    return None


def find_reflection(map):
    reflection_value = scan_horizontally(map)

    if reflection_value:
        return reflection_value

    else:
        reflection_value = scan_vertically(map)

    if not reflection_value:
        raise Exception("no reflection found!")

    return reflection_value


##TODO should be 11 or 12
def get_solution(input):
    reflection_value = 0

    input = collections.deque(input)
    # mirror_map = collections.defaultdict(collections.defaultdict)
    mirror_map = []
    y = 0

    while input:
        line = input.popleft()
        print(f'line {str(y) +" " if y < 10 else y}', line)
        if not line.split():
            print("looking for reflection", mirror_map)
            current_value = find_reflection(mirror_map)
            print("this map gives value", current_value)
            # import pdb; pdb.set_trace()
            reflection_value += current_value
            if not reflection_value:
                raise Exception("no value found!")
            # mirror_map = collections.defaultdict(collections.defaultdict)
            mirror_map = []
            y = 0
            print("line 0  01234567890123456789")
            continue

        # x = 0
        # for char in line:
        # mirror_map[y][x] = char
        mirror_map.append(line)
        # x += 1

        y += 1
    return reflection_value


# example = read_input(f"{problem_id}_example.txt")
# assert(get_solution(example) == example_solution)

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
assert solution > 29849
