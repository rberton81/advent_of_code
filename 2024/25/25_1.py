from collections import defaultdict, deque
from utils.utils import read_input

PIN = "#"

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def pin_len(col):
    pins = 0
    for pin in col:
        if pin == PIN:
            pins += 1
    return pins - 1

def solution(input):
    keys = []
    locks = []
    rows = []

    for line in read_input(input):
        if not line:
            cols = transpose(rows)
            cols = [pin_len(col) for col in cols]
            
            print(f"looking at {rows[0]}")
            if rows[0] == '#####':
                locks.append(cols)
            else:
                keys.append(cols)
            rows = []  
        else:
            rows.append(line)

    if rows:
        cols = transpose(rows)
        cols = [pin_len(col) for col in cols]
        
        print(f"looking at {rows[0]}")
        if rows[0] == '#####':
            locks.append(cols)
        else:
            keys.append(cols)
            
    print(f"keys: {len(keys)}")
    print(f"locks: {len(locks)}")

    import pdb; pdb.set_trace()

    fits = 0 
    for key in keys:
        for lock in locks:
            lock_fits = True
            # import pdb; pdb.set_trace()
            for key_pin, lock_pin in zip(key, lock):
                if key_pin + lock_pin > 5:
                    lock_fits = False
                    break
            if lock_fits:
                fits += 1

        
    print(f"Returning {fits}")
    return fits

assert solution("example.txt") == 3
_solution = solution("input.txt")
print("solution: ", _solution)
assert _solution > 3580
