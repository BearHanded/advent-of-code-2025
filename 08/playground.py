import math
from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def get_distance(a, b):
    a_x, a_y, a_z = a
    b_x, b_y, b_z = b
    return math.sqrt((b_x - a_x)**2+(b_y - a_y)**2+(b_z - a_z)**2)

def build_circuits(filename, max_joins):
    boxes = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]
    potential_connections = []
    for idx, box_a in enumerate(boxes):
        for box_b in boxes[idx+1:]:
            if box_a == box_b:
                continue
            potential_connections.append((get_distance(box_a, box_b), box_a, box_b)) # (Distance, a, b)
    potential_connections.sort()

    circuits = list(map(lambda p: {p}, boxes))
    joins = 0
    while joins < max_joins and len(potential_connections) > 0 and len(circuits) > 1:
        joins += 1 # happens no matter what
        distance, a, b = potential_connections.pop(0)
        matches = []
        for idx, circuit in enumerate(circuits):
            if a in circuit or b in circuit:
                matches.append(idx)
        if len(matches) == 1:
            continue
        circuits[matches[0]] = circuits[matches[0]].union(circuits[matches[1]])
        circuits.pop(matches[1])

    circuits = sorted(circuits, key=lambda i: len(i), reverse=True)
    result = 0 if len(circuits) <= 1 else len(circuits[0]) * len(circuits[1]) * len(circuits[2])
    print("Multiple of 3 largest:", result)
    print("Connections:", joins)
    print("Final Connection", a, b)
    print("Final Connection Distance", a[0] * b[0])

    return result, a[0] * b[0]

# Pt 1
multiplied, distance = build_circuits(TEST_INPUT, 10)
assert_equals(multiplied, 40)
build_circuits(INPUT, 1000)

multiplied, distance = build_circuits(TEST_INPUT, 100000000000000000000000)
assert_equals(distance, 25272)
build_circuits(INPUT, 100000000000000000000000)

