from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def build_map(filename):
    lines = [line.split(" ") for line in file_to_array(filename)]
    connections = {line[0][:-1]: line[1:] for line in lines}
    return connections

def total_routes(filename):
    connections = build_map(filename)
    queue = ["you"]
    successful_routes = 0
    while len(queue) > 0:
        current = queue.pop(0)
        nodes = connections[current]

        for node in nodes:
            if node == "out":
                successful_routes += 1
            else:
                queue.append(node)
    print("Total routes:", total_routes)

    return successful_routes


# Pt 1
assert_equals(total_routes(TEST_INPUT), 5)
total_routes(INPUT)
