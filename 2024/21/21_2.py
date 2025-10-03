import collections
# from functools import cache
from functools import cache
import itertools
from utils.utils import read_input

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
A = "A"

class InvalidPermutation(Exception):
    pass

def get_moves(delta_x, delta_y):
    if delta_x > 0:
        horizontal = RIGHT
    elif delta_x < 0:
        horizontal = LEFT
    else:
        horizontal = None

    if delta_y > 0:
        vertical = DOWN
    elif delta_y < 0:
        vertical = UP
    else:
        vertical = None

    if horizontal and vertical:
        moves = (
            abs(delta_x) * [horizontal] + abs(delta_y) * [vertical] + [A],
            abs(delta_y) * [vertical] + abs(delta_x) * [horizontal] + [A],
        )
    elif horizontal:
        moves = (abs(delta_x) * [horizontal] + [A],)
    elif vertical:
        moves = (abs(delta_y) * [vertical] + [A],)
    else:
        moves = ([A],)

    #TODO right up down left?
    # return tuple(tuple(move) for move in moves)
    return moves


def filter_invalid_moves(permutations, x_start, y_start, invalid_x, invalid_y):
    valid_permutations = []
    for permutation in permutations:
        x, y = x_start, y_start
        try:
            for move in permutation:
                if move == UP:
                    y -= 1
                elif move == DOWN:
                    y += 1
                elif move == LEFT:
                    x -= 1
                elif move == RIGHT:
                    x += 1
                if (x == invalid_x and y == invalid_y):
                    raise InvalidPermutation
        except InvalidPermutation:
            continue            
        valid_permutations.append(permutation)
    return tuple(valid_permutations)

def nested_dict():
    return collections.defaultdict(nested_dict)

def subtract(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]

class NumericPad:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    def __init__(self):
        self.current = A
        self.pad = {
            "7": (0, 0),
            "8": (1, 0),
            "9": (2, 0),
            "4": (0, 1),
            "5": (1, 1),
            "6": (2, 1),
            "1": (0, 2),
            "2": (1, 2),
            "3": (2, 2),
            "0": (1, 3),
            A: (2, 3),

        }

    def go_to(self, target):
        current_cell = self.pad[self.current]
        target_cell = self.pad[target]
        print(f"Trying to go from {self.current}:{current_cell} to {target}:{target_cell}")
        delta_x, delta_y = subtract(target_cell, current_cell)
        must_filter = False
        moves = get_moves(delta_x, delta_y)
        print(f"Moves: {moves}")
        self.current = target

        x_c, y_c = current_cell
        x_t, y_t = target_cell
        must_filter = (x_c == 0 and y_t == 3) or (x_t == 0 and y_c == 3)
        if must_filter:
            moves = filter_invalid_moves(moves, x_c, y_c, 0, 3)
        paths = [(0, tuple(move)) for move in moves]
        return paths


class KeyPad:
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    def __init__(self, idx):
        self.current = A
        self.pad = {
            UP: (1, 0),
            A: (2, 0),
            LEFT: (0, 1),
            DOWN: (1, 1),
            RIGHT: (2, 1),
        }
        self.idx = idx

    def copy(self):
        new_key_pad = KeyPad(self.idx)
        new_key_pad.current = self.current
        return new_key_pad
    
    # @cache
    def go_to(self, target):
        current_cell = self.pad[self.current]
        target_cell = self.pad[target]
        print(f"Trying to go from {self.current}:{current_cell} to {target}:{target_cell}")
        delta_x, delta_y = subtract(target_cell, current_cell)
        moves = get_moves(delta_x, delta_y)
        self.current = target

        x_c, y_c = current_cell
        x_t, y_t = target_cell
        must_filter = (y_c == 0 and x_t == 0) or (x_c == 0 and y_t == 0)
        if must_filter:
            moves = filter_invalid_moves(moves, x_c, y_c, 0, 0)
        return list(moves)

@cache
def get_key_pads_moves(moves, key_pad: KeyPad):
    total_moves = [] 
    for move in moves:
        key_pad_moves = key_pad.go_to(move)
        if not total_moves:
            total_moves = key_pad_moves
        else:
            if len(key_pad_moves) == 1:
                total_moves = [_move + key_pad_moves[0] for _move in total_moves]
            else:
                new_moves = []
                for product in list(itertools.product(total_moves, key_pad_moves)):
                    new_moves.append(product[0] + product[1])
                total_moves = new_moves

    paths = [(key_pad.idx+1, tuple(move)) for move in total_moves]
    return paths

def move_is_best(moves_count, best_move_counts_by_pad_idx, key_pad_idx):
    return best_move_counts_by_pad_idx[key_pad_idx] and moves_count > best_move_counts_by_pad_idx[key_pad_idx]

def solution(input, key_pads_count):
    complexity = 0
    num_pad = NumericPad()
    key_pads = [KeyPad(idx) for idx in range(key_pads_count)]
    _cache = {}
    min_count_by_pad_idx = {}
    processed_paths = set()

    for line in read_input(input):
        code = line.strip()
        code_move_count = 0

        for char in code:
            move_count = float('inf')
            all_num_pad_moves = num_pad.go_to(char)
            paths = collections.deque(all_num_pad_moves)
            
            while paths:
                print(f"length: {len(paths)}")
                # key_pad_idx, path = paths.popleft()
                key_pad_idx, path = paths.pop()
                processed_paths.add(path)

                if key_pad_idx == key_pads_count:
                    move_count = min(move_count, len(path))
                    continue

                key_pad = key_pads[key_pad_idx]
                cache_key = (tuple(path), key_pad.current)
                if cache_key in _cache:
                    paths.extend(_cache[cache_key])
                else:
                    results = get_key_pads_moves(path, key_pad)
                    kept = []
                    for result in results:
                        pad_idx, _moves = result
                        if pad_idx in min_count_by_pad_idx and min_count_by_pad_idx[pad_idx] >= len(_moves):
                            if _moves not in processed_paths:
                                kept.append(result)
                        else:
                            min_count_by_pad_idx[pad_idx] = len(_moves)
                            kept.append(result)
                    _cache[cache_key] = kept 
                    paths.extend(kept)
            
            # import pdb; pdb.set_trace()
            code_move_count += move_count

        int_in_code = int(code[:-1])
        code_complexity = code_move_count * int_in_code
        print(f"Code complexity: {code_move_count}*{int_in_code}={code_complexity}")
        # import pdb; pdb.set_trace()
        complexity += code_complexity 

    print(f"complexity: {complexity}")
    return complexity

# assert solution("example.txt", 25) == 126384
_solution = solution("input.txt", 3)
print("solution: ", _solution)
