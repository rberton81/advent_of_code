from utils.utils import read_input


def solve_line(line):
    sum = 0
    for range in line.split(","):
        print(f"Looking at range: {range}")
        # start, end = map(int, range.split("-"))
        start, end = range.split("-")

        if len(start) % 2 != 0:
            print('Odd number of digits, getting closest number with even number of digits')
            start = str(10**(len(start)))
            if int(start) > int(end):
                print("New number outside of range")
                continue
            print(f"Starting from {start}")

        candidate_part = start[:len(start)//2]
        print(f"Initial candidate part: {candidate_part}")
        candidate = int(f"{candidate_part}{candidate_part}")
        print(f"candidate: {candidate}")
        import pdb; pdb.set_trace()

        while candidate < int(start):
            candidate_part = str(int(candidate_part)+1)
            candidate = int(f"{candidate_part}{candidate_part}")
            print(f"candidate: {candidate}")
        
        while candidate <= int(end):
            sum += candidate
            print(f"Added {candidate} to {sum}")
            import pdb; pdb.set_trace()
            candidate_part = str(int(candidate_part)+1)
            candidate = int(f"{candidate_part}{candidate_part}")
            print(f"candidate: {candidate}")
        print(f'Done, {candidate} >= {end}')
    
    print(f"Sum is {sum}")
    return sum

def solve(input):
    sum = 0
    for line in read_input(input):
        sum += solve_line(line)
    return sum

example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
assert solve_line(example) == 1227775554

solution = solve("input.txt")
assert solution > 28715393940