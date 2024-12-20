import collections
from utils.utils import read_input

WALL = "#"
TRACK = "."
START = "S"
END = "E"


class Map:
    def __init__(self, map, start, end):
        self.map = map
        self.start = start
        self.end = end

    class Cell:
        def __init__(self, pos, is_wall=False, is_start=False, is_end=False):
            self.pos = pos
            self.is_wall = is_wall
            self.is_start = is_start
            self.is_end = is_end
            self.path_score = 0

        def __repr__(self):
            return f"{self.pos}->{self.path_score}"

        def is_current_best_path(self, previous_cell):
            if self.is_start:
                return False
            return not self.is_wall and (
                not self.path_score or previous_cell.path_score + 1 < self.path_score
            )

    @staticmethod
    def build_map(lines):
        map = collections.defaultdict()
        start, end = None, None

        for y, line in enumerate(lines):
            map[y] = collections.defaultdict()
            for x, char in enumerate(line):
                if char == WALL:
                    map[y][x] = Map.Cell((x, y), is_wall=True)
                elif char == END:
                    map[y][x] = Map.Cell((x, y), is_end=True)
                    end = (x, y)
                elif char == START:
                    map[y][x] = Map.Cell((x, y), is_start=True)
                    start = (x, y)
                else:
                    map[y][x] = Map.Cell((x, y))
        return Map(map, start, end)

    def set_track_scores(self):
        paths = collections.deque([self.get(*self.start)])
        tracks = set()
        while paths:
            cell = paths.popleft()
            tracks.add(cell)
            if cell.pos == self.end:
                break
            paths.extend(self.explore_cell(cell))
        return tracks

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
                if cell.is_wall:
                    row.append(WALL)
                elif cell.is_start:
                    row.append(START)
                elif cell.is_end:
                    row.append(END)
                else:
                    row.append(TRACK)
            print(" ".join(row))
        return ""

    def explore_cell(self, cell: Cell):
        x, y = cell.pos
        next_paths = []

        for offset in (-1, 1):
            horizontal = self.get(x + offset, y)
            vertical = self.get(x, y + offset)
            for other in (horizontal, vertical):
                if other and not other.is_wall:
                    if other.is_current_best_path(cell):
                        other.path_score = cell.path_score + 1
                        next_paths.append(other)

        return next_paths

    def get_tracks_within_distance(self, track, max_distance):
        x, y = track.pos
        cells__distance = []

        for offset_h in range(-max_distance, max_distance + 1):
            for offset_v in range(
                -max_distance + abs(offset_h), max_distance - abs(offset_h) + 1
            ):
                other = self.get(x + offset_h, y + offset_v)
                if not other or other.is_wall:
                    continue
                distance = abs(offset_h) + abs(offset_v)
                cells__distance.append((other, distance))

        return cells__distance

    def get_shortcuts(self, track, max_distance, min_time_saved):
        shortcuts = 0
        for reachable_track, distance in self.get_tracks_within_distance(
            track, max_distance
        ):
            time_saved = reachable_track.path_score - track.path_score - distance
            if time_saved >= min_time_saved:
                shortcuts += 1
        return shortcuts


def solution(input, max_cheat_distance, time_save_target):
    map = Map.build_map(read_input(input))
    tracks = map.set_track_scores()
    shortcuts = 0
    for track in tracks:
        shortcuts += map.get_shortcuts(track, max_cheat_distance, time_save_target)
    return shortcuts


assert solution("example.txt", 20, 50) == 285
_solution = solution("input.txt", 20, 100)
print("solution: ", _solution)
