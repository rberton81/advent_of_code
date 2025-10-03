from utils.utils import read_input
import networkx as nx

def create_general_graph(edges):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph

def solution(input):
    edges = set()
    for line in read_input(input):
        edge = tuple(line.split("-"))
        edges.add(edge)

    graph = create_general_graph(edges)
    cliques = list(nx.find_cliques(graph))
    max_length = max(len(lst) for lst in cliques)
    max_length_lists = [lst for lst in cliques if len(lst) == max_length]

    if len(max_length_lists) == 1:
        longest = max_length_lists[0]
        code = ",".join(sorted(longest))
        return code

assert solution("example.txt") == "co,de,ka,ta"
_solution = solution("input.txt")
print("solution: ", _solution)
