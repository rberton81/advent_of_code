import collections
import itertools
import re
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
    
    if len(valid_permutations) == len(permutations):
        raise Exception("No permutations were filtered")
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
        paths = [(0, move) for move in moves]
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
    
    # def go_to(self, target, moves_count):
    #     current_cell = self.pad[self.current]
    #     target_cell = self.pad[target]
    #     print(f"Trying to go from {self.current}:{current_cell} to {target}:{target_cell}")
    #     delta_x, delta_y = subtract(target_cell, current_cell)
    #     moves = get_moves(delta_x, delta_y)
    #     # print(f"Moves: {moves}")
    #     self.current = target

    #     x_c, y_c = current_cell
    #     x_t, y_t = target_cell
    #     must_filter = (y_c == 0 and x_t == 0) or (x_c == 0 and y_t == 0)
    #     if must_filter:
    #         moves = filter_invalid_moves(moves, x_c, y_c, 0, 0)
    #     paths = [(len(move) + moves_count, self.idx+1, move) for move in moves]
    #     return paths
    
    def go_to(self, target):
        current_cell = self.pad[self.current]
        target_cell = self.pad[target]
        print(f"Trying to go from {self.current}:{current_cell} to {target}:{target_cell}")
        delta_x, delta_y = subtract(target_cell, current_cell)
        moves = get_moves(delta_x, delta_y)
        # print(f"Moves: {moves}")
        self.current = target

        x_c, y_c = current_cell
        x_t, y_t = target_cell
        must_filter = (y_c == 0 and x_t == 0) or (x_c == 0 and y_t == 0)
        if must_filter:
            moves = filter_invalid_moves(moves, x_c, y_c, 0, 0)
        return list(moves)
    
def get_key_pads_moves(moves, key_pad: KeyPad):
    print(f"Getting keypad moves for {moves}")
    total_moves = [] 
    for move in moves:
        key_pad_moves = key_pad.go_to(move)
        print(f"key_pad_moves: {key_pad_moves}")
        if not total_moves:
            print('setting__')
            total_moves = key_pad_moves
        else:
            #TODO i want to create new paths
            if len(key_pad_moves) == 1:
                # print(f"total_moves: {total_moves} / {key_pad_moves}")
                total_moves = [_move + key_pad_moves[0] for _move in total_moves]
            else:
                # print(f"**** total_moves: {total_moves} / {key_pad_moves}")
                new_moves = []
                for product in list(itertools.product(total_moves, key_pad_moves)):
                    new_moves.append(product[0] + product[1])
                total_moves = new_moves
                # print(f"total_moves after: {total_moves}")

    paths = [(key_pad.idx+1, move) for move in total_moves]
    # print(f"paths: {paths}")
    # import pdb; pdb.set_trace()
    return paths

def move_is_best(moves_count, best_move_counts_by_pad_idx, key_pad_idx):
    return best_move_counts_by_pad_idx[key_pad_idx] and moves_count > best_move_counts_by_pad_idx[key_pad_idx]

def solution(input, key_pads_count):
    complexity = 0

    num_pad = NumericPad()
    key_pads = [KeyPad(idx) for idx in range(key_pads_count)]

    for line in read_input(input):
        code = line.strip()
        print(f"Entering code {code}")
        
        code_move_count = 0
        for char in code:
            move_count = float('inf')
            print(f" ***************** Entering digit {char}")
            all_num_pad_moves = num_pad.go_to(char)

            paths = collections.deque(all_num_pad_moves)
            while paths:
                key_pad_idx, path = paths.popleft()
                print(f"Processing {path} / {key_pad_idx}")
                # import pdb; pdb.set_trace()
                
                if key_pad_idx == key_pads_count:
                    move_count = min(move_count, len(path))
                    continue

                paths.extend(get_key_pads_moves(path, key_pads[key_pad_idx].copy()))
                print(f'paths is now {paths}')

            print("Entered digit.")
            print(f"length: {move_count}")
            # import pdb; pdb.set_trace()
            code_move_count += move_count

        int_in_code = int(code[:-1])
        code_complexity = code_move_count * int_in_code
        print(f"Code complexity: {code_move_count}*{int_in_code}={code_complexity}")
        # import pdb; pdb.set_trace()
        complexity += code_complexity 

    print(f"complexity: {complexity}")
    return complexity

assert solution("example.txt", 2) == 126384
_solution = solution("input.txt", 2)
print("solution: ", _solution)
