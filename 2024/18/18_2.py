import collections
from utils.utils import read_input


CORRUPTED = "#"
EMPTY_SPACE = "."

class Map:
    def __init__(self, map):
        self.map = map

    class Cell:
        def __init__(self, pos, is_corrupted=False):
            self.pos = pos
            self.is_corrupted = is_corrupted
            self.path_score = 0

        def __repr__(self):
            return f"{self.pos}"
        
        def is_current_best_path(self, previous_cell):
            return not self.is_corrupted and (not self.path_score or previous_cell.path_score + 1 < self.path_score)
        
    @staticmethod
    def build_map(bytes, max_x, max_y):
        map = collections.defaultdict()
        for y in range(max_y):
            map[y] = collections.defaultdict()
            for x in range(max_x):
                if (x, y) in bytes:
                    map[y][x] = Map.Cell((x, y), is_corrupted=True)
                else:
                    map[y][x] = Map.Cell((x, y))
        return Map(map)
    
    def reset_scores(self):
        for x__cell in self.map.values():
            for cell in x__cell.values():
                cell.path_score = 0

    def get(self, x, y) -> Cell:
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None

    def print(self):
        for y, x__cell in self.map.items():
            row = []
            for x, cell in x__cell.items():
                if cell.is_corrupted:
                    row.append(CORRUPTED)
                else:
                    row.append(EMPTY_SPACE)
            print(" ".join(row))
        return ""
    
    def explore_cell(self, cell:Cell):
        x, y = cell.pos
        next_paths = []

        for offset in (-1, 1):
            horizontal = self.get(x + offset, y)
            vertical = self.get(x, y + offset)
            for other in (horizontal, vertical):
                if other and not other.is_corrupted:
                    if other.is_current_best_path(cell):
                        other.path_score = cell.path_score + 1
                        next_paths.append(other)
                    
        return next_paths
    
def solution(input, max_x, max_y, max_bytes):
    bytes, extra_bytes = set(), collections.deque()
    lines= read_input(input)
    for line in lines:
        x, y = line.split(",")
        if len(bytes) < max_bytes:
            bytes.add((int(x), int(y)))
        else:
            extra_bytes.append((int(x), int(y)))

    map = Map.build_map(bytes, max_x, max_y)
    while extra_bytes:
        added_byte = extra_bytes.popleft()
        bytes.add(added_byte)
        map.get(*added_byte).is_corrupted = True
        map.reset_scores()
        path_queue = collections.deque([map.get(0,0)])
        can_exit = False

        while path_queue:
            cell = path_queue.popleft()
            if cell.pos == (max_x-1,max_y-1):
                can_exit = True
                break
            next_paths= map.explore_cell(cell)
            path_queue += next_paths

        if not can_exit:
            return added_byte
    
assert solution("example.txt", 7, 7, 12) == (6,1)
_solution = solution("input.txt", 71, 71, 1024)
print("solution: ", _solution)