import collections
import os
import math

example_solution = 405
problem_id = os.path.basename(__file__).split(".")[0].split("_")[0]


def read_input(path, by_line=True, in_one_line=False):
    with open(path) as file:
        lines = file.readlines()
        if by_line:
            return [line.rstrip("\n") for line in lines]
        if in_one_line:
            return "".join(lines)
        return lines


def validate_reflection(start, map, direction):
    print("validating")
    # import pdb; pdb.set_trace()

    i = 0
    max_count = 0
    if direction == "H":
        while True and max_count < 1000:
            try:
                print(f"checking {map[start+i]} and {map[start-i-1]}")
                if map[start + i] != map[start - i - 1]:
                    print("not reflection!")
                    print(f"lists not same: {map[start+i]} and {map[start-i-1]}")
                    return False
            except IndexError:
                print(f"{start} is reflection!")
                return True
            i += 1
            if start - i - 1 < 0:
                return True
            max_count += 1
    elif direction == "V":
        while True and max_count < 1000:
            try:
                for y in range(len(map)):
                    print(f"checking {map[y][start+i]} and {map[y][start-i-1]}")
                    if map[y][start + i] != map[y][start - i - 1]:
                        print("not reflection!")
                        print(f"chars in {start+i, y} and {start-i-1, y} are different")
                        return False
            except IndexError:
                print("is reflection!")
                return True
            i += 1
            if start - i - 1 < 0:
                return True
            max_count += 1
            print("foo")


def scan_horizontally(map):
    # previous_row = []
    # current_row = []
    print("scanning horizontally")
    if len(map) % 2 == 0:
        up, down = len(map) - 2, len(map) - 1
        print(f"up {up} down {down}")
        if map[up] == map[down]:
            print("init found candidate reflection horizontally", up)
            if validate_reflection(up, map, "H"):
                return up * 100  ##TODO check
    else:
        up, down = math.floor(len(map) / 2), math.ceil(len(map) / 2)

    # import pdb; pdb.set_trace()

    while True:
        print(f"up {up} down {down}")
        if up >= 0:
            print(f"up -> comparing {map[up]} and {map[up+1]}")
        if down < len(map):
            print(f"down -> comparing {map[down]} and {map[down-1]}")
        if up >= 0 and map[up] == map[up + 1]:
            print("up found candidate reflection horizontally", up)
            if validate_reflection(up + 1, map, "H"):  ##TODO maybe +1
                return (up + 1) * 100
        if down < len(map) and map[down] == map[down - 1]:
            print("down found candidate reflection horizontally", down)
            if validate_reflection(down, map, "H"):
                return down * 100

        up -= 1
        down += 1

        if up < 0 and down >= len(map):
            return None
            # raise Exception("cant find shit!")

        # import pdb; pdb.set_trace()
        print("foo")

    # for y in range(len(map)):
    #     for x in range(len(map[0])):
    #         current_row.append(map[y][x])

    #     if current_row == previous_row:
    #         print('found candidate reflection horizontally', y)
    #         if validate_reflection(y, map, "H"):
    #             # return y-1
    #             return y * 100

    #     previous_row = current_row
    #     current_row = []

    # return None


def scan_vertically(map):
    print("scanning vertically")

    if len(map[0]) % 2 == 0:
        left, right = len(map[0]) - 2, len(map[0]) - 1
        print(f"up {left} down {right}")
        if map[left] == map[right]:
            print("init found candidate reflection vertically", left)
            if validate_reflection(left, map, "H"):
                return left  ##TODO check
    else:
        left, right = math.floor(len(map[0]) / 2), math.ceil(len(map[0]) / 2)

    # import pdb; pdb.set_trace()

    while True:
        print(f"left {left} right {right}")

        left_is_reflection = True
        right_is_reflection = True

        for y in range(len(map)):
            if left >= 0:
                print(f"left -> comparing {map[y][left]} and {map[y][left+1]}")
            if right < len(map[0]):
                try:
                    # print(f"right {right} map {map[y]}")
                    print(f"right -> comparing {map[y][right]} and {map[y][right-1]}")
                except Exception as err:
                    import pdb

                    pdb.set_trace()
                    print("foo")
            if left >= 0 and map[y][left] != map[y][left + 1]:
                # print('left not same!')
                left_is_reflection = False

            if right < len(map[0]) and map[y][right] != map[y][right - 1]:
                print("right not same!")
                # import pdb; pdb.set_trace()
                right_is_reflection = False

            if not left_is_reflection and right_is_reflection:
                break

        if left_is_reflection:
            print("left found candidate reflection vertically", left)
            if validate_reflection(left + 1, map, "V"):
                return left + 1
            print("left was not reflection")

        if right_is_reflection:
            print("right found candidate reflection vertically", right)
            if validate_reflection(right, map, "V"):
                return right
            print("right was not reflection")

        left -= 1
        right += 1

        if left < 0 and right >= len(map[0]):
            return None
            # raise Exception("cant find shit!")

        # import pdb; pdb.set_trace()
        print("foo")

    ##FIX OLD
    # previous_column = []
    # current_column = []
    # for x in range(len(map[0])):
    #     for y in range(len(map)):
    #         current_column.append(map[y][x])

    #     if current_column == previous_column:
    #         print('found candidate reflection vertically', x)
    #         if validate_reflection(x, map, "V"):
    #             # return (x-1) * 100
    #             return x

    #     previous_column = current_column
    #     current_column = []

    print("no vertical reflection")
    return None


def find_reflection(map):
    reflection_value = scan_horizontally(map)

    if reflection_value:
        # if scan_vertically(map):
        #     print('two values!!!!!!')
        #     import pdb; pdb.set_trace()
        return reflection_value

    else:
        reflection_value = scan_vertically(map)

    if not reflection_value:
        raise Exception("no reflection found!")

    return reflection_value


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
            # import pdb; pdb.set_trace()
            print("line 0  0123456789123456789")
            continue

        # x = 0
        # for char in line:
        # mirror_map[y][x] = char
        mirror_map.append(line)
        # x += 1

        y += 1
    return reflection_value


example = read_input(f"{problem_id}_example.txt")
assert get_solution(example) == example_solution

input = read_input(f"{problem_id}_input.txt")
solution = get_solution(input)
print(f"solution: {solution}")
