from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
TEST_INPUT_2 = "test_input_2.txt"
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
    print("Total routes:", successful_routes)

    return successful_routes

def svr_routes(filename):
    connections = build_map(filename)
    queue = [("svr", set())]
    successful_routes = 0
    while len(queue) > 0:
        current, visited = queue.pop(0)
        nodes = connections[current]

        for node in nodes:
            if node == "out":
                print(visited)
                if "dac" in visited and "fft" in visited:
                    successful_routes += 1
            else:
                new_visited = visited.copy()
                new_visited.add(node)
                queue.append((node, new_visited))
    print("Total routes:", successful_routes)

    return successful_routes

# Pt 1
assert_equals(total_routes(TEST_INPUT), 5)
total_routes(INPUT)

# Pt 1
assert_equals(svr_routes(TEST_INPUT_2), 2)
svr_routes(INPUT)
# bad: 708