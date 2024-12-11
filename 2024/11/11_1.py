from utils.utils import read_input

def blink(stones):
    stones_after_blink = []
    for stone in stones:
        print(f'looking at stone {stone}')
        if int(stone) == 0:
            print('Stone is 0, turning it to 1')
            stones_after_blink.append("1")
        elif len(stone) % 2 ==0:
            print('splitting stone into 2')
            left_stone = str(int(stone[:len(stone)//2]))
            right_stone = str(int(stone[len(stone)//2:]))
            print(f'splitting stone into 2: {left_stone} and {right_stone}')
            stones_after_blink += [left_stone, right_stone]
        else:
            print('multiplying by 2024')
            stones_after_blink.append(str(int(stone) * 2024))

    print(f"stones_after_blink: {stones_after_blink}")
    return stones_after_blink

def solution(input):
    stone_count = 0
    for stone in read_input(input)[0].split():
        stones = [stone]
        for i in range(25):
            print(f"blink {i}")
            stones = blink(stones)
        print(f"Stone generated {len(stones)} stones!")
        stone_count += len(stones)
    return stone_count
    
assert solution("example.txt") == 55312
print("solution: ", solution("input.txt"))
