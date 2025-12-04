from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"
DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

def find_rolls(rolls):
    targets = []
    for y, row in enumerate(rolls):
        for x, cell in enumerate(row):
            if cell is not "@":
                continue

            nearby = 0
            for direction in DIRS:
                y2 = y + direction[0]
                x2 = x + direction[1]
                if y2 < 0 or y2 >= len(rolls) or x2 < 0 or x2 >= len(row):
                    continue
                if rolls[y2][x2] == "@":
                    nearby += 1
            if nearby < 4:
                targets.append((y, x))
    return targets

def get_accessible_rolls(filename):
    rows = file_to_array(filename)
    accessible = find_rolls(rows)
    print("Accessible: ", len(accessible))
    return len(accessible)

def repeated_removals(filename):
    rows = [list(row) for row in file_to_array(filename)]
    total = 0
    while True:
        accessible = find_rolls(rows)
        total += len(accessible)

        for (y, x) in accessible:
            rows[y][x] = "."
        if len(accessible) == 0:
            break

    print("Removed", total)
    return total


assert_equals(get_accessible_rolls(TEST_INPUT), 13)
get_accessible_rolls(INPUT)

assert_equals(repeated_removals(TEST_INPUT), 43)
repeated_removals(INPUT)
