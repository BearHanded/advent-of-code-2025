from requests.packages import target

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

def intersects(tile_edge, area_edge):
    print(tile_edge)
    t1, t2 = sorted(tile_edge)
    a1, a2 = sorted(area_edge)

    # print("-> ", t1, t2)
    # print("-> ", a1, a2)

    # if area_edge is horizontal and tile is vertical
    if a1[0] < t1[0] < a2[0] and a1[0] < t2[0] < a2[0] and \
        t1[1] < a1[1] < t2[1] and t1[1] < a2[1] < t2[1]:
        print("HIT, Horizontal", tile_edge, area_edge)
        return True
    elif a1[1] < t1[1] < a2[1] and a1[1] < t2[1] < a2[1] and \
        t1[0] < a1[0] < t2[0] and t1[0] < a2[0] < t2[0]: # rotate
        print("HIT, Vertical", tile_edge, area_edge)
        return True

    return False

# Lightweight version of our future search that will just check the corners vs their row
def check_corners(a, b, outer_tiles):
    a_row_tile_xs = [t[0] for t in outer_tiles if t[1] == a[1]]
    b_row_tile_xs = [t[0] for t in outer_tiles if t[1] == b[1]]

    return len(a_row_tile_xs) == 0 or len(b_row_tile_xs) == 0 \
        or (min(a[0], b[0]) < min(a_row_tile_xs)) or (max(a[0], b[0]) > max(a_row_tile_xs)) \
        or (min(a[0], b[0]) < min(b_row_tile_xs)) or (max(a[0], b[0]) > max(b_row_tile_xs))


def find_largest_inside(filename):
    tiles = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]
    tiles.append(tiles[0])
    outer_tiles = set()
    outer_segments = set()

    previous = tiles[0]
    outer_tiles.add(previous)
    outer_segments.add((tiles[-1], tiles[0]))
    min_x = 9999999
    max_x = 0

    # build edges
    for tile in tiles[1:]:
        outer_tiles.update(connect_points(previous, tile))
        outer_segments.add((previous, tile))
        previous = tile
        min_x = min(tile[0], min_x)
        max_x = max(tile[0], max_x)

    largest_area = 0
    # consider fits
    for idx, (a_x, a_y) in enumerate(tiles):
        print(f"Working {idx}/{len(tiles)}")
        potential_areas = [(max(largest_area, (abs(p[0] - a_x) + 1) * (abs(p[1] - a_y) + 1)), p) for p in tiles[idx+1:]]

        for potential_area, (b_x, b_y) in sorted(potential_areas, reverse=True):
            if potential_area <= largest_area:
                continue
            if check_corners((a_x, a_y), (b_x, b_y), outer_tiles):
                continue
            print("...")

            # Todo optimize? do we need all of these?
            # {(a_x, a_y), (a_x, b_y), (b_x, a_y), (b_x, b_y)}
            area_segments =  [((a_x, a_y), (a_x, b_y)), ((a_x, b_y), (b_x, b_y)), ((a_x, a_y), (b_x, a_y)), ((b_x, a_y), (b_x, b_y))]
            inside_fit = True



            # area_edges = connect_points((a_x, a_y), (a_x, b_y))
            # area_edges.update(connect_points((b_x, a_y), (b_x, b_y)))
            # target_edges = area_edges | outer_tiles

            for area_segment in area_segments:
                for outer_segment in outer_segments:
                    if intersects(outer_segment, area_segment):
                        inside_fit = False
                        break
            # for y in range(min(a_y, b_y), max(a_y, b_y) + 1):
            #     on_area_edge = False
            #     on_tile_edge = False
            #     inside_area = False
            #     inside_tiles = False
            #
            #     x_targets = {x_candidate for (x_candidate, y_candidate) in target_edges if y_candidate == y}
            #     x_targets.update([i+1 for i in x_targets]) # allow 1 piece of whitespace to trigger latch
            #     x_targets = sorted([i for i in x_targets if i <= max_x]) # cut it off at end of area, we don't need more
            #
            #     for x in x_targets: # todo this range
            #     # for x in range(min_x, max_x + 2): # todo this range
            #         # Check area
            #         if (x, y) in area_edges:
            #             on_area_edge = not on_area_edge
            #         elif on_area_edge:
            #             # left an edge, flip, unlatch
            #             on_area_edge = False
            #             inside_area = not inside_area
            #
            #         # Check tiles
            #         if (x, y) in outer_tiles:
            #             on_tile_edge = True
            #         elif on_tile_edge:
            #             # left an edge, flip, unlatch
            #             on_tile_edge = False
            #             inside_tiles = not inside_tiles # left an edge, flip
            #
            #         if (on_area_edge or inside_area) and not (on_tile_edge or inside_tiles):
            #             inside_fit = False
            #             break
            #     if not inside_fit:
            #         break
            if inside_fit:
                print("   Candidate:", potential_area)
                largest_area = potential_area
                break

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