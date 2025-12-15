from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def total_fit(filename):
    lines = file_to_array(filename)
    shape_counter = 0
    shape_areas = []
    for line in lines[:30]: # both inputs only have 5 shapes
        if ":" in line:
            shape_counter = 0
            continue
        if line == "":
            shape_areas.append(shape_counter)
            continue
        shape_counter += line.count("#")

    fits = 0
    for line in lines[30:]:
        chunks = line.split(":")
        boxes = [int(i) for i in chunks[1][1:].split(" ")]
        width, height = [int(i) for i in chunks[0].split("x")]
        area = width * height

        estimated_sizes = [i*shape_areas[idx] for idx, i in enumerate(boxes)]
        total_estimate = sum(estimated_sizes)
        if total_estimate <= area:
            fits += 1

    print("total fit:", fits)
    return fits

# Pt 1
# assert_equals(total_fit(TEST_INPUT), 2)
total_fit(INPUT)

