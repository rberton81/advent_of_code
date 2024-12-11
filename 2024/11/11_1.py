from utils.utils import read_input

def blink(stones):
    stones_after_blink = []
    for stone in stones:
        if int(stone) == 0:
            stones_after_blink.append("1")
        elif len(stone) % 2 ==0:
            left_stone = str(int(stone[:len(stone)//2]))
            right_stone = str(int(stone[len(stone)//2:]))
            stones_after_blink += [left_stone, right_stone]
        else:
            stones_after_blink.append(str(int(stone) * 2024))
    return stones_after_blink

def solution(input):
    stone_count = 0
    for stone in read_input(input)[0].split():
        stones = [stone]
        for i in range(25):
            stones = blink(stones)
        stone_count += len(stones)
    return stone_count
    
assert solution("example.txt") == 55312
print("solution: ", solution("input.txt"))
