from collections import defaultdict
from utils.utils import read_input
from visualization import Visualizable

PAPER_CHAR = "@"
class Map(Visualizable):
    class Cell:
        def __init__(self, x, y, is_paper, parent_map):
            self.x = x
            self.y = y
            self.is_paper = is_paper
            self.removal_time = None
            self.parent_map: Map = parent_map

        def __repr__(self):
            return f"Cell({self.x}, {self.y}, is_paper={self.is_paper})"
        
        def is_accessible(self):
            adjacent_papers = 0
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if x_offset == 0 and y_offset == 0:
                        continue

                    try:
                        neighbor = self.parent_map.get(self.x + x_offset, self.y + y_offset)
                    except IndexError:
                        continue
                    if neighbor.is_paper:
                        adjacent_papers += 1
                    if adjacent_papers >= 4:
                        return False
            return True

    def __init__(self, lines):
        self.map = defaultdict(dict)
        x = 0
        for line in lines:
            y = 0
            for char in line:
                is_paper = char == PAPER_CHAR
                self.map[y][x] = Map.Cell(x, y, is_paper, self)
                y += 1
            x += 1

        self.height = x
        self.width = y


    def get(self, x, y):
        if x < 0 or x > self.height - 1 or y < 0 or y > self.width -1:
            raise IndexError(f"Out of bounds access at ({x}, {y})")
        return self.map[y % self.height][x % self.width]
    
    def get_accessible_papers(self):
        accessible_papers = []
        for x in range(self.height):
            for y in range(self.width):
                cell = self.get(x, y)
                if cell.is_paper and cell.is_accessible():
                    accessible_papers.append(cell)
        return accessible_papers
    
    def remove_accessible_papers(self):
        accessible_papers = self.get_accessible_papers()
        removed_count = 0
        for cell in accessible_papers:
            cell.is_paper = False
            cell.removal_time = 5
            removed_count += 1
        return removed_count


def solve(input):
    map = Map(read_input(input))
    return map.visualize_pygame(frame_action=map.remove_accessible_papers)

# assert solve("example.txt") == 43
print(f"solution = {solve('input.txt')}")