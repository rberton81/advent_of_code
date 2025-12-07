from utils.utils import read_input
import os 
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))


class Map():
    def __init__(self, lines):
        x = 0
        rows = []
        self.start_beam = None
        for line in lines:
            y = 0
            row = []
            for char in line:
                if is_start(char):
                    self.start_beam = (x+1, y)
                if self.start_beam is not None and x == self.start_beam[0] and y == self.start_beam[1]:
                    row.append("|")
                else:
                    row.append(char)
                y += 1
            rows.append(row)
            x += 1

        self.height = x
        self.width = y
        self.map = rows
    
def is_start(cell_char):
    return cell_char == "S"
def is_beam(cell_char):
    return cell_char == "|"
def is_splitter(cell_char):
    return cell_char == "^"
def is_empty(cell_char):
    return cell_char == "."

def clone_timeline(timeline):
    return [row[:] for row in timeline] 

def process_timeline(current_position, map):
    current_x, current_y = current_position
    next_row_id = current_x + 1

    if next_row_id >= len(map):
        return
    
    cell_below = map[next_row_id][current_y]

    if is_splitter(cell_below):
        left_col_id = current_y - 1
        right_col_id = current_y + 1
        can_split_right, can_split_left = True, True

        if right_col_id >= len(map[0]):
            can_split_right = False
        if left_col_id < 0:
            can_split_left = False

        if can_split_left:
            if can_split_right:
                yield True, (next_row_id, right_col_id)
            yield False, (next_row_id, left_col_id)
        elif can_split_right:
            yield False, (next_row_id, right_col_id)
    elif is_empty(cell_below):
        yield False, (next_row_id, current_y)


def get_new_timelines(current_position, map, memo):
    if current_position in memo:
        return memo[current_position]
    
    new_timelines = 0
    for is_new_timeline, new_position in process_timeline(current_position, map):
        if is_new_timeline:
            new_timelines += 1
        new_timelines += get_new_timelines(new_position, map, memo)
    memo[current_position] = new_timelines
    return new_timelines

def solve(input):
    timelines_count = 1
    map = Map(read_input(input))
    timelines_count += get_new_timelines(map.start_beam, map.map, {})

    return timelines_count

def print_map(rows):
    for row in rows:
        print(" ".join([cell for cell in row]))
    return ""

assert solve(CURRENT_DIR + "/example.txt") == 40
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")