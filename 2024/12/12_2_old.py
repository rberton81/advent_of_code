import collections
from utils.utils import read_input

DEBUG_CHAR = "A"

class Map:
    class Directions:
        VERTICAL = "V"
        HORIZONTAL = "H"

    def __init__(self, lines):
        self.map = self.build_map(lines)

    class Cell:
        def __init__(self, pos, char, was_visited=False):
            self.was_visited = was_visited
            self.pos = pos
            self.char = char
            self.sides = set()

        def __repr__(self):
            return f"{self.pos} -> {self.char} / sides: {self.sides}"
        
    def get(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except KeyError:
            return None
        
    def get_cells(self):
        for x__cell in self.map.values():
            for cell in x__cell.values():
                yield cell

    def visit_neighbors(self, cell, x, y, area, side_count):
        neighbor = self.get(x, y)
        if neighbor and not neighbor.was_visited and neighbor.char == cell.char:
            neighbor.was_visited = True
            area += 1
            side_count += self.set_sides_and_get_unique_count(neighbor)
            area, side_count = self.get_area_and_side_count(neighbor, area=area, side_count=side_count)
        return area, side_count

    def get_area_and_side_count(self, cell: Cell, area, side_count):
        x, y = cell.pos

        area, side_count = self.visit_neighbors(cell, x, y+1, area, side_count) 
        area, side_count = self.visit_neighbors(cell, x-1, y, area, side_count) 
        area, side_count = self.visit_neighbors(cell, x, y-1, area, side_count) 
        area, side_count = self.visit_neighbors(cell, x+1, y, area, side_count) 

        print('returning', area, side_count)
        # import pdb; pdb.set_trace()
        return area, side_count


    def look_for_unique_sides(self, cell, x, y, direction):
        neighbor = self.get(x, y)
        if cell.char == DEBUG_CHAR:
            print(f'__ other in dir {direction}, pos {x, y} is {neighbor}')

        if not neighbor or neighbor.char != cell.char:
            cell.sides.add((x, y))
            print(f"added side {(x, y)}")
            side_is_unique = True

            for offset in (-1, 1):
                _x, _y = cell.pos
                x_side, y_side = x, y
                if direction == self.Directions.VERTICAL:
                    _y += offset
                    y_side = _y
                else:
                    _x += offset
                    x_side = _x
                side_neighbor = self.get(_x, _y)

                if cell.char == DEBUG_CHAR:
                    print('looking at neighbor', side_neighbor)
                
                if side_neighbor and side_neighbor.char == cell.char:
                    print(f"is {(x_side, y_side)} in sides?", (x_side, y_side) in side_neighbor.sides)
                    if (x_side, y_side) in side_neighbor.sides:
                        side_is_unique = False
            if side_is_unique:
                print('**** added a unique side')
                import pdb; pdb.set_trace()
                return 1
        return 0

    def set_sides_and_get_unique_count(self, cell:Cell):
        x, y = cell.pos
        unique_sides = 0
        print(f'+++++ LOOKING AT {x,y}')
        unique_sides += (
            self.look_for_unique_sides(cell, x, y+1, direction=self.Directions.HORIZONTAL) 
            + self.look_for_unique_sides(cell, x-1, y, direction=self.Directions.VERTICAL) 
            + self.look_for_unique_sides(cell, x, y-1, direction=self.Directions.HORIZONTAL) 
            + self.look_for_unique_sides(cell, x+1, y, direction=self.Directions.VERTICAL)
        )

        # unique_sides += (
        #     self.look_for_unique_sides(cell, x, y+1, direction=self.Directions.VERTICAL) 
        #     + self.look_for_unique_sides(cell, x-1, y, direction=self.Directions.HORIZONTAL) 
        #     + self.look_for_unique_sides(cell, x, y-1, direction=self.Directions.VERTICAL) 
        #     + self.look_for_unique_sides(cell, x+1, y, direction=self.Directions.HORIZONTAL)
        # )

        # if cell.char == DEBUG_CHAR:
        #     print('after')
        #     import pdb; pdb.set_trace()

        return unique_sides
    

    # def set_sides_and_get_unique_count(self, cell:Cell):
    #     x, y = cell.pos
    #     unique_sides = 0
    #     print(f'+++++ LOOKING AT {x,y}')

    #     for offset in (-1, 1):
    #         y_other = y+offset
    #         vertical = self.get(x, y_other)

    #         if cell.char == DEBUG_CHAR:
    #             print('__ other is', vertical)
    #         if not vertical or vertical.char != cell.char:
    #             side_is_unique = True
    #             for x_offset in (-1, 1):
    #                 x_other = x + x_offset
    #                 side_neighbor = self.get(x_other, y)

    #                 if cell.char == DEBUG_CHAR:
    #                     print('looking at neighbor', side_neighbor)
    #                 if side_neighbor and side_neighbor.char == cell.char:
    #                     print(f"is {(x_other, y_other)} in sides?", (x_other, y_other) in side_neighbor.sides)
    #                     if (x_other, y_other) in side_neighbor.sides:
    #                         side_is_unique = False
    #             if side_is_unique:
    #                 print('**** added a unique horizontal side')
    #                 import pdb; pdb.set_trace()
    #                 unique_sides += 1

    #         x_other = x + offset
    #         horizontal = self.get(x_other, y)  
    #         if cell.char == DEBUG_CHAR:
    #             print('__ other is', horizontal)

    #         if not horizontal or horizontal.char != cell.char:
    #             side_is_unique = True
    #             for y_offset in (-1, 1):
    #                 y_other = y + y_offset
    #                 side_neighbor = self.get(x, y_other)

    #                 if cell.char == DEBUG_CHAR:
    #                     print('looking at neighbor', side_neighbor)
    #                 if side_neighbor and side_neighbor.char == cell.char:
    #                     if (x_other, y_other) in side_neighbor.sides:
    #                         side_is_unique = False
    #             if side_is_unique:
    #                 print(' **** added a unique vertical side')
    #                 import pdb; pdb.set_trace()
    #                 unique_sides += 1 

    #     # if cell.char == DEBUG_CHAR:
    #     #     print('after')
    #     #     import pdb; pdb.set_trace()

    #     return unique_sides

    # def set_cell_sides(self, cell:Cell):
    #     x, y = cell.pos
    #     for offset in (-1, 1):
    #         y_other = y+offset
    #         vertical = self.get(x, y_other)
    #         if not vertical or vertical.char != cell.char:
    #             cell.sides.add((x, y_other))

    #         x_other = x + offset
    #         horizontal = self.get(x_other, y)  
    #         if not horizontal or horizontal.char != cell.char:
    #             cell.sides.add((x_other, y))

    def build_map(self, lines):
        map = collections.defaultdict()
        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                map[y][x] = Map.Cell((x, y), char)
        return map
    
    def print(self):
        for y, x__cell in self.map.items():
            row = []
            for x, cell in x__cell.items():
                row.append(cell.char)
            print(" ".join(row))
        return ""

def solution(input):
    total_price = 0
    
    map = Map(read_input(input))

    for y, x__cell in map.map.items():
        row = []
        for x, cell in x__cell.items():
            if cell.was_visited:
                continue
            cell.was_visited = True
            area, side_count = map.get_area_and_side_count(cell, area=1, side_count=map.set_sides_and_get_unique_count(cell))
            print(f'area, sides: {area}, {side_count}')
            plant_price = area * side_count
            print(f'contributing: {plant_price}')
            total_price += plant_price
            previous_plant = cell.char


    print('total_price', total_price)
    return total_price
    
# assert solution("example.txt") == 1206
# assert solution("example_2.txt") == 436
# assert solution("example_3.txt") == 236
# assert solution("example_4.txt") == 80
assert solution("example_5.txt") == 368
# _solution = solution("input.txt")
# print("solution: ", _solution)
# assert _solution > 1319850
