from collections import defaultdict, deque
from utils.utils import read_input

def calculate_next_secret(current_secret):
    current_secret = (current_secret * 64) ^ current_secret
    current_secret = current_secret % 16777216
    current_secret = (current_secret // 32) ^ current_secret
    current_secret = current_secret % 16777216
    current_secret = (current_secret * 2048) ^ current_secret
    current_secret = current_secret % 16777216
    return current_secret

def update_price_changes(last_four_price_changes, price_change):
    if len(last_four_price_changes) < 4:
        last_four_price_changes.append(price_change)
    else:
        last_four_price_changes.popleft()
        last_four_price_changes.append(price_change)

def find_common_highest_sequences_and_sum(sequences_by_price_by_secret, unique_sequences_counts):
    highest_price = 0
    _sorted = sorted(unique_sequences_counts.items(), key=lambda item: item[1], reverse=True)

    for sequence, count in _sorted:
        sequence_candidate = sequence
        sequence_price = 0

        for sequences_by_price in sequences_by_price_by_secret.values():
            for i in range(9, 0, -1):
                if sequence_candidate in sequences_by_price[i]:
                    sequences_by_price[i].remove(sequence_candidate)
                    sequence_price += i
                    break

        if sequence_price > highest_price:
            highest_price = sequence_price

    return highest_price

def solution(input):
    sequences_by_price_by_secret = defaultdict(lambda: defaultdict(set))

    for idx, line in enumerate(read_input(input)):
        next_secret = None 
        previous_price = int(str(int(line))[-1] )
        
        last_four_price_changes = deque()
        unique_sequences_counts = defaultdict(int)
        
        seen_sequences = set()
        
        for _ in range(2000):
            next_secret = calculate_next_secret(next_secret or int(line))
            new_price = int(str(next_secret or int(line))[-1])
            price_change = new_price - previous_price

            update_price_changes(last_four_price_changes, price_change)

            if len(last_four_price_changes) == 4 and new_price > 0:
                unique_sequences_counts[tuple(last_four_price_changes)] += 1
                if tuple(last_four_price_changes) not in seen_sequences:
                    sequences_by_price_by_secret[idx][new_price].add(tuple(last_four_price_changes))
                    seen_sequences.add(tuple(last_four_price_changes))
            
            previous_price = new_price
    
    bananas = find_common_highest_sequences_and_sum(sequences_by_price_by_secret, unique_sequences_counts)
    return bananas

assert solution("example_1.txt") == 23
_solution = solution("input.txt")
print("solution: ", _solution)