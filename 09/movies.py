import math
from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def find_larges_area(filename):
    tiles = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]

    largest_area = 0

    for idx, (a_x, a_y) in enumerate(tiles):
        for b_x, b_y in tiles[idx + 1:]:
            largest_area = max(largest_area, (abs(b_x - a_x) + 1) * (abs(b_y - a_y) + 1))
    print("Largest area:", largest_area)
    return largest_area

# Pt 1
assert_equals(find_larges_area(TEST_INPUT), 50)
find_larges_area(INPUT)