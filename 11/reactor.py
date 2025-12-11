from functools import cache

from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
TEST_INPUT_2 = "test_input_2.txt"
INPUT = "input.txt"

def build_map(filename):
    global connections
    lines = [line.split(" ") for line in file_to_array(filename)]
    connections = {line[0][:-1]: line[1:] for line in lines}

def total_routes(filename):
    build_map(filename)
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

connections = dict()

@cache
def find_out(current, visited_dac, visited_fft):
    successful_paths = 0
    nodes = connections[current]
    visited_dac = visited_dac or current == "dac"
    visited_fft = visited_fft or current == "fft"
    for node in nodes:
        if node == "out":
            if visited_dac and visited_fft:
                successful_paths += 1
            continue
        successful_paths += find_out(node, visited_dac, visited_fft)
    return successful_paths

def svr_routes(filename):
    find_out.cache_clear()
    build_map(filename)
    successful_routes = find_out("svr", False, False)

    print("Total routes:", successful_routes)

    return successful_routes

# Pt 1
assert_equals(total_routes(TEST_INPUT), 5)
total_routes(INPUT)

# Pt 1
assert_equals(svr_routes(TEST_INPUT_2), 2)
svr_routes(INPUT)
