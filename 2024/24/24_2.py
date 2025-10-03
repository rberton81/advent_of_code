from collections import defaultdict, deque
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
            print(f"Resolved {self}")
            self.value_1 = value_1
            self.value_2 = value_2
            self.value_out = value_by_node[self.out]
            self.is_resolved = True
        else:
            print("Cant resolve yet!")
        return value_by_node
    
    # def resolve(self, value_by_node):
    #     if self.in_1 in value_by_node and self.in_2 in value_by_node:
    #         value_1 = value_by_node[self.in_1]
    #         value_2 = value_by_node[self.in_2]
    #         if self.operator == Operator.AND:
    #             value_by_node[self.out] = value_1 & value_2
    #         elif self.operator == Operator.OR:
    #             value_by_node[self.out] = value_1 | value_2
    #         elif self.operator == Operator.XOR:
    #             value_by_node[self.out] = value_1 ^ value_2
    #         print(f"Resolved {self}")
    #         self.is_resolved = True
    #     else:
    #         print("Cant resolve yet!")
    #     return value_by_node
    
    def swap(self, other_gate:"Gate"):
        self.out = other_gate.out
        other_gate.out = self.out
    
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

def to_binary(integer):
    binary = []
    while integer:
        binary.append(integer % 2)
        integer = integer // 2
    return binary

def solution(input):
    value_by_node, gates, roots = get_init_values__gates__roots(input)

    binary_x = {}
    binary_y = {}
    for node, value in value_by_node.items():
        if "x" in node:
            idx = int(node[1:])
            binary_x[idx] = value
        elif "y" in node:
            idx = int(node[1:])
            binary_y[idx] = value

    x = 0
    for idx, value in binary_x.items():
        x += value * (2 ** idx)
    y = 0
    for idx, value in binary_y.items():
        y += value * (2 ** idx)

    print(f"We're sunning {x} and {y}")

    expected_z = to_binary(x+y)
    expected_z = {i: expected_z[i] for i in range(len(expected_z))}
    print(f"Expected z: {expected_z}")

    gates_graph = defaultdict(list)

    # for root in roots:
    #     value_by_node = root.resolve(value_by_node)
    # print('resolved roots', value_by_node)

    # for root in roots:
    #     for gate in gates:
    #         print(f"Checking if {root.out} is in {gate.in_1} or {gate.in_2}")
    #         if root.out in (gate.in_1, gate.in_2):
    #             gates_graph[root].append(gate)
    #     value_by_node = root.resolve(value_by_node)

    _gates = deque(gates)
    while _gates:
        gate = _gates.popleft()
        for other_gate in _gates:
            print(f"Checking if {gate.out} is in {other_gate.in_1} or {other_gate.in_2}")
            if gate.out in (other_gate.in_1, other_gate.in_2):
                gates_graph[gate].append(other_gate)
    
    for gate in gates:
        if gate not in gates_graph:
            test = gate.resolve(value_by_node)
            value_1 = value_by_node[gate.in_1]
            value_2 = value_by_node[gate.in_2]

            import pdb; pdb.set_trace()
        else:
            pass
        

    print('computed graph')
    import pdb; pdb.set_trace()
        
    # while gates:
    #     gate = gates.popleft()
    #     value_by_node = gate.resolve(value_by_node)
    #     if not gate.is_resolved:
    #         gates.append(gate)

    binary_values = {}
    for node, value in value_by_node.items():
        if "z" in node:
            print(f"{node}: {value}")
            idx = int(node[1:])
            binary_values[idx] = value

    print(f"binary_values: {binary_values}")
    import pdb; pdb.set_trace()    
    number = 0
    for idx, value in binary_values.items():
        number += value * (2 ** idx)

    import pdb; pdb.set_trace()

    return number

assert solution("example_1.txt") == "z00,z01,z02,z05"
# _solution = solution("input.txt")
# print("solution: ", _solution)
