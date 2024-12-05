from utils.utils import DirectedGraph, read_input

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

def get_middle_element(page_update):
    middle_index = len(page_update) // 2
    return page_update[middle_index]

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

    middle_pages_sum = 0
    for page_update in page_updates:
        if is_valid(page_update, page_relationships):
            middle_pages_sum += int(get_middle_element(page_update))

    return middle_pages_sum


assert solution("example.txt") == 143
print("solution: ", solution("input.txt"))
