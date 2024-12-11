from utils.utils import read_input

def blink_at_stone(stone):
    stones_after_blink = []
    if int(stone) == 0:
        stones_after_blink.append("1")
    elif len(stone) % 2 == 0:
        left_stone = str(int(stone[:len(stone)//2]))
        right_stone = str(int(stone[len(stone)//2:]))
        stones_after_blink += [left_stone, right_stone]
    else:
        stones_after_blink.append(str(int(stone) * 2024))
    return stones_after_blink

def blink_at_each_stone_and_count(stones, cache, blinks_count=None): 
    if blinks_count == 0:
        return len(stones)

    key = (tuple(stones), blinks_count)
    if key in cache:
        return cache[key]

    stones_count = 0
    for stone in stones:
        new_stones = blink_at_stone(stone)
        stones_count += blink_at_each_stone_and_count(new_stones, cache, blinks_count=blinks_count-1)

    cache[key] = stones_count
    return stones_count

def solution(input):
    init_stones = read_input(input)[0].split()
    cache = {}

    stones_count = blink_at_each_stone_and_count(init_stones, cache, blinks_count=75)
    return stones_count

print("solution: ", solution("input.txt"))
