import collections
from utils.utils import read_input


class Map:
    def __init__(self, lines):
        self.map = self.build_map(lines)

    class Cell:
        def __init__(self, pos, char, was_visited=False):
            self.was_visited = was_visited
            self.pos = pos
            self.char = char

        def __repr__(self):
            return f"{self.pos} -> {self.char}"

    def get_area_and_perimeter(self, cell: Cell, area, perimeter):
        x, y = cell.pos
        for offset in (-1, 1):
            try:
                vertical = self.map[y + offset][x]
                if not vertical.was_visited and vertical.char == cell.char:
                    vertical.was_visited = True
                    area += 1
                    perimeter += self.get_cell_perimeter(vertical)
                    area, perimeter = self.get_area_and_perimeter(
                        vertical, area=area, perimeter=perimeter
                    )
            except KeyError:
                pass

            try:
                horizontal = self.map[y][x + offset]
                if not horizontal.was_visited and horizontal.char == cell.char:
                    horizontal.was_visited = True
                    area += 1
                    perimeter += self.get_cell_perimeter(horizontal)
                    area, perimeter = self.get_area_and_perimeter(
                        horizontal, area=area, perimeter=perimeter
                    )
            except KeyError:
                pass

        return area, perimeter

    def get_cell_perimeter(self, cell: Cell):
        perimeter = 4
        x, y = cell.pos

        for offset in (-1, 1):
            try:
                vertical = self.map[y + offset][x]
                if vertical.char == cell.char:
                    perimeter -= 1
            except KeyError:
                pass

            try:
                horizontal = self.map[y][x + offset]
                if horizontal.char == cell.char:
                    perimeter -= 1
            except KeyError:
                pass

        return perimeter

    def build_map(self, lines):
        map = collections.defaultdict()
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                map[y][x] = Map.Cell((x, y), char)
        return map


def solution(input):
    total_price = 0

    map = Map(read_input(input))

    for x__cell in map.map.values():
        for cell in x__cell.values():
            if cell.was_visited:
                continue
            cell.was_visited = True
            area, perimeter = map.get_area_and_perimeter(
                cell, area=1, perimeter=map.get_cell_perimeter(cell)
            )
            plant_price = area * perimeter
            total_price += plant_price

    return total_price


_solution = solution("input.txt")
print("solution: ", _solution)
