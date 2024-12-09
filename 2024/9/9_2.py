import collections
from utils.utils import read_input


class File:
    def __init__(self, idx, length, pos):
        self.idx = idx
        self.length = length
        self.pos = pos

    def __repr__(self):
        return "".join([str(self.idx)] * self.length)

    def get_checksum(self):
        check_sum = 0
        pos = self.pos
        for _ in range(self.length):
            check_sum += self.idx * pos
            pos += 1
        return check_sum


class DiskSpace:
    def __init__(self, length, pos):
        self.length = length
        self.pos = pos

    def __repr__(self):
        repr = "".join(["."] * self.length)
        return f"{repr} at {self.pos}"


def solution(input):
    files = collections.deque()
    disk_spaces = collections.deque()

    is_file = True
    file_idx = 0
    position = 0
    line = collections.deque(read_input(input)[0])
    while line:
        length = int(line.popleft())
        if is_file:
            files.append(File(file_idx, length, position))
            file_idx += 1
            position += length
        else:
            disk_spaces.append(DiskSpace(length, position))
            position += length
        is_file = not is_file

    checksum = 0
    while files:
        file = files.pop()
        file_was_fit = False

        for disk_space in disk_spaces:
            if disk_space.pos > file.pos:
                break
            if disk_space.length >= file.length:
                file.pos = disk_space.pos
                checksum += file.get_checksum()
                disk_space.length -= file.length
                if not disk_space.length:
                    disk_spaces.remove(disk_space)
                disk_space.pos += file.length
                file_was_fit = True
                break
        if not file_was_fit:
            checksum += file.get_checksum()

    return checksum


assert solution("example.txt") == 2858
print("solution: ", solution("input.txt"))
