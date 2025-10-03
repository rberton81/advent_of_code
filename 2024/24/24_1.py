from collections import deque
from utils.utils import read_input

class Operator:
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

class Gate:
    def __init__(self, in_1, in_2, operator, out):
        self.in_1 = in_1
        self.in_2 = in_2
        self.operator = operator
        self.out = out
        self.is_resolved = False

    def __repr__(self):
        return f"{self.in_1} {self.operator} {self.in_2} -> {self.out}"

    def resolve(self, value_by_node):
        if self.in_1 in value_by_node and self.in_2 in value_by_node:
            value_1 = value_by_node[self.in_1]
            value_2 = value_by_node[self.in_2]
            if self.operator == Operator.AND:
                value_by_node[self.out] = value_1 & value_2
            elif self.operator == Operator.OR:
                value_by_node[self.out] = value_1 | value_2
            elif self.operator == Operator.XOR:
                value_by_node[self.out] = value_1 ^ value_2
            self.is_resolved = True
        return value_by_node
    
def get_init_values__gates__roots(input):
    init_value_by_node = {}
    roots = []
    gates = []

    for line in read_input(input):
        if not line:
            continue
        
        if ":" in line:
            node, init_value = line.split(":")
            init_value = int(init_value)
            init_value_by_node[node] = init_value
        else:
            in_1, operator, in_2, _, out = line.split()
            gate = Gate(in_1, in_2, operator, out)
            if any(["x" in in_1, "y" in in_1] ) and any(["x" in in_2, "y" in in_2]) :
                roots.append(gate)
            gates.append(gate)
    
    return init_value_by_node, gates, roots

def solution(input):
    value_by_node, gates, roots = get_init_values__gates__roots(input)

    for root in roots:
        value_by_node = root.resolve(value_by_node)
        
    gates = deque(gates)
    while gates:
        gate = gates.popleft()
        value_by_node = gate.resolve(value_by_node)
        if not gate.is_resolved:
            gates.append(gate)

    binary_values = {}
    for node, value in value_by_node.items():
        if "z" in node:
            idx = int(node[1:])
            binary_values[idx] = value
    
    number = 0
    for idx, value in binary_values.items():
        number += value * (2 ** idx)

    return number

assert solution("example.txt") == 2024
_solution = solution("input.txt")
print("solution: ", _solution)
