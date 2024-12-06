from collections import deque
from utils.utils import DirectedGraph, get_middle_element, read_input

def is_valid(page_update, page_relationships: DirectedGraph):
    previous_page = None
    for page in page_update:
        if not previous_page:
            previous_page = page
            continue
        try:
            if page not in page_relationships.graph[previous_page]:
                return False
        except KeyError:
            return False
        previous_page = page
    return True

def get_misplaced_pages__valid_sequence(page_update, page_relationships: DirectedGraph):
    misplaced_pages = deque()
    valid_sequence = deque(page_update)
    previous_page = None
    _page_update = deque(page_update)
    replay = False

    while _page_update:
        if replay:
            replay = False
        else:
            page = _page_update.popleft()

        if not previous_page:
            previous_page = page
            continue
        
        try:
            if page not in page_relationships.graph[previous_page]:
                misplaced_pages.append(page)
                valid_sequence.remove(page)
                continue
        except KeyError:
            misplaced_pages.append(previous_page)
            valid_sequence.remove(previous_page)
            
            if previous_page == page_update[0]:
                previous_page = None
            else: 
                replay = True
                previous_page = valid_sequence[valid_sequence.index(page)-1]
            continue

        previous_page = page
    
    return misplaced_pages, valid_sequence

def make_valid(misordered_pages, page_relationships: DirectedGraph):
    misplaced_pages, valid_sequence = get_misplaced_pages__valid_sequence(misordered_pages, page_relationships)

    while misplaced_pages:
        misplaced_page = misplaced_pages.popleft()
        for page in valid_sequence.copy():
            try:
                if page in page_relationships.graph[misplaced_page]:
                    valid_sequence.insert(valid_sequence.index(page), misplaced_page)
                    break
            except KeyError:
                valid_sequence.append(misplaced_page)
                break
    
    return valid_sequence

def solution(input):
    page_orders = []
    page_updates = []

    for line in read_input(input):
        if "|" in line:
            page_orders.append(line.split("|"))
        elif line:
            page_updates.append(line.split(","))

    page_relationships = DirectedGraph()
    for from_vertex, to_vertex in page_orders:
        page_relationships.add_edge(from_vertex, to_vertex)

    page_relationships.display()
    invalid_updates = [page_update for page_update in page_updates if not is_valid(page_update, page_relationships)]
    
    middle_pages_sum = 0
    for invalid_update in invalid_updates:
        valid_update = make_valid(invalid_update, page_relationships)
        middle_pages_sum += int(get_middle_element(valid_update))
    return middle_pages_sum

# assert solution("example.txt") == 123
print("solution: ", solution("input.txt"))
