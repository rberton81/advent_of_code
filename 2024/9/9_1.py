import collections
from utils.utils import read_input


class File:
    def __init__(self, idx, length):
        self.idx = idx
        self.length = length

    def __repr__(self):
        return "".join([str(self.idx)] * self.length)

    def get_checksum(self, pos):
        check_sum = 0
        for _ in range(self.length):
            check_sum += self.idx * pos
            pos += 1
        return check_sum, pos


class EmptySpace:
    def __init__(self, length):
        self.length = length

    def __repr__(self):
        return "".join(["."] * self.length)


def solution(input):
    files_and_spaces = []
    files = collections.deque()

    is_file = True
    file_idx = 0
    line = collections.deque(read_input(input)[0])
    while line:
        length = int(line.popleft())
        if is_file:
            file = File(file_idx, length)
            files_and_spaces.append(file)
            files.append(file)
            file_idx += 1
            is_file = False
        else:
            files_and_spaces.append(EmptySpace(length))
            is_file = True

    checksum = 0
    pos_idx = 0
    file = files.pop()
    for file_or_space in files_and_spaces:
        if isinstance(file_or_space, File):
            file_check_sum, pos_idx = file_or_space.get_checksum(pos_idx)
            checksum += file_check_sum
            if files:
                files.popleft()
        elif isinstance(file_or_space, EmptySpace):
            while file_or_space.length and files:
                if files and not file.length:
                    file = files.pop()

                if file_or_space.length <= file.length:
                    file.length -= file_or_space.length
                    for _ in range(file_or_space.length):
                        checksum += file.idx * pos_idx
                        pos_idx += 1
                    file_or_space.length = 0
                else:
                    file_or_space.length -= file.length
                    for _ in range(file.length):
                        checksum += file.idx * pos_idx
                        pos_idx += 1
                    file.length = 0
    return checksum


assert solution("example.txt") == 1928
print("solution: ", solution("input.txt"))
