from itertools import combinations
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
    groups_of_3 = set()

    for clique in cliques:
        if len(clique) < 3:
            continue
        else:
            combs = combinations(clique, 3)
            for comb in list(combs):
                groups_of_3.add(tuple(sorted(comb)))

    candidates_groups = []    
    for group in groups_of_3:
        for computer in group:
            if computer.startswith("t"):
                candidates_groups.append(group)
                break

    return len(candidates_groups)

assert solution("example.txt") == 7
_solution = solution("input.txt")
print("solution: ", _solution)
