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
    # draws a rect composed by 2 points, but if they're in a line, it's just a line
    points = set()
    x_range = [min(a[0], b[0]), max(a[0], b[0]) + 1]
    y_range = [min(a[1], b[1]), max(a[1], b[1]) + 1]
    points.update((x, a[1]) for x in range(*x_range))
    points.update((x, b[1]) for x in range(*x_range))
    points.update((a[0], y) for y in range(*y_range))
    points.update((b[0], y) for y in range(*y_range))

    return points

def intersects(tile_edge, area_edge):
    # Check whether two line segments intersect, only works horizontal and vertical
    t1, t2 = sorted(tile_edge)
    a1, a2 = sorted(area_edge)

    # if area_edge is horizontal and tile is vertical
    if a1[0] < t1[0] < a2[0] and a1[0] < t2[0] < a2[0] and \
        t1[1] < a1[1] < t2[1] and t1[1] < a2[1] < t2[1]:
        return True
    elif a1[1] < t1[1] < a2[1] and a1[1] < t2[1] < a2[1] and \
        t1[0] < a1[0] < t2[0] and t1[0] < a2[0] < t2[0]: # rotate
        return True

    return False

def corners_outside(a, b, outer_tiles):
    # Lightweight spot check to just make sure 4 corners are within the bounds of all outer edges of the shape
    if a[1] not in outer_tiles or b[1] not in outer_tiles:
        return True
    a_row_tile_xs = outer_tiles[a[1]]
    b_row_tile_xs = outer_tiles[b[1]]

    return len(a_row_tile_xs) == 0 or len(b_row_tile_xs) == 0 \
        or (min(a[0], b[0]) < min(a_row_tile_xs)) or (max(a[0], b[0]) > max(a_row_tile_xs)) \
        or (min(a[0], b[0]) < min(b_row_tile_xs)) or (max(a[0], b[0]) > max(b_row_tile_xs))


def find_largest_inside(filename):
    tiles = [tuple(int(i) for i in row.split(",")) for row in file_to_array(filename)]
    tiles.append(tiles[0])
    outer_tiles = dict()
    outer_segments = set()

    previous = tiles[0]
    outer_segments.add((tiles[-1], tiles[0]))

    # build edges
    tile_loop = tiles[1:]
    for tile in tile_loop:
        points = connect_points(previous, tile)
        for p in points:
            if p[1] not in outer_tiles:
                outer_tiles[p[1]] = list([p[0]])
            else:
                outer_tiles[p[1]].append(p[0])
        outer_segments.add((previous, tile))
        previous = tile

    largest_area = 0

    # consider fits
    for idx, (a_x, a_y) in enumerate(tiles):
        potential_areas = [(max(largest_area, (abs(p[0] - a_x) + 1) * (abs(p[1] - a_y) + 1)), p) for p in tiles[idx+1:]]

        for potential_area, (b_x, b_y) in sorted(potential_areas, reverse=True):
            if potential_area <= largest_area or corners_outside((a_x, a_y), (b_x, b_y), outer_tiles):
                continue

            area_segments =  [((a_x, a_y), (a_x, b_y)), ((a_x, b_y), (b_x, b_y)), ((a_x, a_y), (b_x, a_y)), ((b_x, a_y), (b_x, b_y))]
            inside_fit = True
            for area_segment in area_segments:
                for outer_segment in outer_segments:
                    if intersects(outer_segment, area_segment):
                        inside_fit = False
                        break
            if inside_fit:
                print("   Candidate:", potential_area)
                largest_area = potential_area
                break

    print("Largest area:", largest_area)
    return largest_area

# Pt 1
assert_equals(find_largest_area(TEST_INPUT), 50)
find_largest_area(INPUT)

# Pt 1
assert_equals(find_largest_inside(TEST_INPUT), 24)
find_largest_inside(INPUT)