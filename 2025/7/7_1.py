from utils.utils import read_input
import os 
from collections import defaultdict
CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))


class Map():
    class Cell:
        BEAM_CHAR = "|"
        START_CHAR = "S"
        SPLITTER_CHAR = "^"
        EMPTY_CHAR = "."

        def __init__(self, x, y, char, parent_map):
            self.x = x
            self.y = y
            self.char = char
            self.removal_time = None
            self.parent_map: Map = parent_map

        def is_empty(self):
            return self.char == self.EMPTY_CHAR
        
        def is_beam(self):
            return self.char == self.BEAM_CHAR
        
        def is_start(self):
            return self.char == self.START_CHAR
        
        def is_splitter(self):
            return self.char == self.SPLITTER_CHAR

        def __repr__(self):
            return f"Cell({self.x}, {self.y}, char={self.char})"
        
    def __init__(self, lines):
        self.map = defaultdict(dict)
        x = 0
        for line in lines:
            y = 0
            for char in line:
                self.map[x][y] = Map.Cell(x, y, char, self)
                y += 1
            x += 1

        self.height = x
        self.width = y


    def get(self, x, y):
        if x < 0 or x > self.height - 1 or y < 0 or y > self.width -1:
            raise IndexError(f"Out of bounds access at ({x}, {y})")
        return self.map[y % self.height][x % self.width]
    


def solve(input):
    split_counts = 0
    map = Map(read_input(input))
    for row_id, row in enumerate(map.map.values()):
        for col_id, cell in enumerate(row.values()):
            print(f"Processing cell at ({row_id}, {col_id}): {cell}")
            if cell.is_start():
                print(f"Start initiated at ({row_id+1}, {col_id})")
                new_beam = map.map[row_id+1][col_id]
                new_beam.char = Map.Cell.BEAM_CHAR

            if cell.is_beam():
                print(f"Beam found at ({row_id}, {col_id})")
                next_row_id = row_id + 1
                if next_row_id >= map.height:
                    print(f"Beam at ({row_id}, {col_id}) cannot split, reached bottom of map")
                    continue
                cell_below = map.map[next_row_id][col_id]

                if cell_below.is_splitter():
                    left_col_id = col_id - 1
                    right_col_id = col_id + 1
                    new_beam_left, new_beam_right = None, None

                    if left_col_id < 0:
                        print(f"Beam at ({row_id}, {col_id}) cannot split left, out of bounds")
                    else:
                        new_beam_left = map.map[next_row_id][left_col_id]
                        if not new_beam_left.is_beam():
                            print(f"Beam at ({row_id}, {col_id}) splits left to ({next_row_id}, {left_col_id})")
                            new_beam_left.char = Map.Cell.BEAM_CHAR
                    
                    if right_col_id >= map.width:
                        print(f"Beam at ({row_id}, {col_id}) cannot split right, out of bounds")
                    else:
                        new_beam_right = map.map[next_row_id][right_col_id]
                        if not new_beam_right.is_beam():
                            print(f"Beam at ({row_id}, {col_id}) splits right to ({next_row_id}, {right_col_id})")
                            new_beam_right.char = Map.Cell.BEAM_CHAR
                    
                    if new_beam_left or new_beam_right:
                        split_counts += 1
                elif cell_below.is_empty():
                    print(f"Beam at ({row_id}, {col_id}) continues down to ({next_row_id}, {col_id})")
                    cell_below.char = Map.Cell.BEAM_CHAR

        print(f"beam_counts so far: {split_counts}")
    return split_counts


assert solve(CURRENT_DIR + "/example.txt") == 21
solution = solve(CURRENT_DIR + "/input.txt")
print(f"solution = {solution}")