from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def find_largest_area(filename):
    tiles = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]

    largest_area = 0

    for idx, (a_x, a_y) in enumerate(tiles):
        for b_x, b_y in tiles[idx + 1:]:
            largest_area = max(largest_area, (abs(b_x - a_x) + 1) * (abs(b_y - a_y) + 1))
    print("Largest area:", largest_area)
    return largest_area

def connect_points(a, b):
    # draws the left and right edges of a rectangle defined by 2 points
    points = set()
    x_range = [min(a[0], b[0]), max(a[0], b[0]) + 1]
    y_range = [min(a[1], b[1]), max(a[1], b[1]) + 1]
    points.update((x, a[1]) for x in range(*x_range))
    points.update((x, b[1]) for x in range(*x_range))
    points.update((a[0], y) for y in range(*y_range))
    points.update((b[0], y) for y in range(*y_range))

    return points

def find_largest_inside(filename):
    tiles = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]
    tiles.append(tiles[0])
    outer_tiles = set()

    previous = tiles[0]
    outer_tiles.add(previous)
    min_x = 9999999
    max_x = 0

    # build edges
    for tile in tiles[1:]:
        outer_tiles.update(connect_points(previous, tile))
        previous = tile
        min_x = min(tile[0], min_x)
        max_x = max(tile[0], max_x)

    largest_area = 0
    # consider fits
    for idx, (a_x, a_y) in enumerate(tiles):
        print(f"Working {idx}/{len(tiles)}")
        potential_areas = [(max(largest_area, (abs(p[0] - a_x) + 1) * (abs(p[1] - a_y) + 1)), p) for p in tiles[idx+1:]]
        for potential_area, (b_x, b_y) in sorted(potential_areas, reverse=True):
            if potential_area < largest_area:
                continue

            area_edges = connect_points((a_x, a_y), (b_x, b_y))
            all_edges = area_edges | outer_tiles

            inside_fit = True
            for y in range(min(a_y, b_y), max(a_y, b_y) + 1):
                on_area_edge = False
                on_tile_edge = False
                inside_area = False
                inside_tiles = False

                row_area_xs = [e[0] for e in area_edges if e[1] == y]
                row_tiles_xs = [t[0] for t in outer_tiles if t[1] == y]
                # print(row_area_xs, row_tiles_xs)
                if len(row_tiles_xs) == 0 or (min(row_area_xs) < min(row_tiles_xs)) or (max(row_area_xs) > max(row_tiles_xs)):
                    inside_fit = False
                    break

                x_targets = {x_candidate for (x_candidate, y_candidate) in all_edges if y_candidate == y}
                x_targets.update([i+1 for i in x_targets]) # allow 1 piece of whitespace to trigger latch
                x_targets = sorted([i for i in x_targets if i <= max_x]) # cut it off at end of area, we don't need more

                for x in x_targets: # todo this range
                # for x in range(min_x, max_x + 2): # todo this range
                    # Check area
                    if (x, y) in area_edges:
                        on_area_edge = True
                    elif on_area_edge:
                        # left an edge, flip, unlatch
                        on_area_edge = False
                        inside_area = not inside_area

                    # Check tiles
                    if (x, y) in outer_tiles:
                        on_tile_edge = True
                    elif on_tile_edge:
                        # left an edge, flip, unlatch
                        on_tile_edge = False
                        inside_tiles = not inside_tiles # left an edge, flip

                    if (on_area_edge or inside_area) and not (on_tile_edge or inside_tiles):
                        inside_fit = False
                        break
                if not inside_fit:
                    break
            if inside_fit:
                print("   Candidate:", potential_area)
                largest_area = potential_area

    # print(outer_tiles)
    print("Largest area:", largest_area)
    return largest_area

# Pt 1
assert_equals(find_largest_area(TEST_INPUT), 50)
find_largest_area(INPUT)
#
# weird = set()
# weird.update(connect_points((1,1), (3,3)))
# weird.update(connect_points((3,3), (1,1)))

# print("weird:",weird)

# Pt 1
assert_equals(find_largest_inside(TEST_INPUT), 24)
find_largest_inside(INPUT)