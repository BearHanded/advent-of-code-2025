from functools import cache
from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def fire_beams(filename):
    grid = [list(row) for row in file_to_array(filename)]
    start_x = grid[0].index("S")
    collisions = set()
    beam_queue = {(0, start_x)}

    while beam_queue:
        beam_y, beam_x = beam_queue.pop()
        if not (0 <= beam_x <= len(grid[0])):
            continue

        while True:
            beam_y = beam_y + 1
            if beam_y >= len(grid):
                break

            next_cell = grid[beam_y][beam_x]
            if next_cell == ".":
                continue
            elif next_cell == "^":
                collisions.add((beam_y, beam_x))
                beam_queue.add((beam_y, beam_x-1))
                beam_queue.add((beam_y, beam_x+1))
                break

    print("Total collisions:", len(collisions))
    return len(collisions)


timeline_grid = [[]]

@cache
def fire_beam_across_time(beam_y, beam_x):
    if not (0 <= beam_x <= len(timeline_grid[0])):
        return 0
    total = 0
    while True:
        beam_y = beam_y + 1
        if beam_y >= len(timeline_grid):
            total += 1 # end of timeline
            break

        next_cell = timeline_grid[beam_y][beam_x]
        if next_cell == ".":
            continue
        elif next_cell == "^":
            total += fire_beam_across_time(beam_y, beam_x-1)
            total += fire_beam_across_time(beam_y, beam_x+1)
            break
    return total

def total_timelines(filename):
    global timeline_grid
    timeline_grid = [list(row) for row in file_to_array(filename)]
    start_x = timeline_grid[0].index("S")
    total = fire_beam_across_time(0, start_x)

    print("Total timelines:", total)
    return total

# Pt 1
assert_equals(fire_beams(TEST_INPUT), 21)
fire_beams(INPUT)

# Pt 1
assert_equals(total_timelines(TEST_INPUT), 40)
total_timelines(INPUT)
