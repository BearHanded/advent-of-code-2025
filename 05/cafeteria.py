from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def total_fresh(filename):
    lines = file_to_array(filename)
    divider = lines.index("")
    fresh = [tuple(int(i) for i in endpoints.split("-")) for endpoints in lines[:divider]]
    available = [int(i) for i in lines[divider + 1:]]

    total = 0

    for ingredient in available:
        for fresh_range in fresh:
            if ingredient in range(fresh_range[0], fresh_range[1] + 1):
                total += 1
                break
    print("Total Fresh:", total)
    return total


def merge_fresh(fresh):
    merging = True
    while merging:
        merging = False
        for a_idx, a in enumerate(fresh):
            for b_idx, b in enumerate(fresh[a_idx + 1:]):
                print("comparing", a, b)
                # lower bound inside or upper bound inside
                if b[0] <= a[0] <= b[1] or b[0] <= a[1] <= b[1]:
                    merging = True
                    merged = (min(a[0], b[0]), max(a[1], b[1]))
                    fresh[a_idx] = merged
                    fresh.pop(a_idx + b_idx + 1)
                    print("Merging,", a, b)
                    print("   Merged:", merged)
                    break
            if merging:
                break
    return fresh

def all_fresh(filename):
    lines = file_to_array(filename)
    divider = lines.index("")
    fresh = [tuple(int(i) for i in endpoints.split("-")) for endpoints in lines[:divider]]
    fresh = merge_fresh(fresh)

    total = 0
    for fresh_range in fresh:
        total += fresh_range[1] - fresh_range[0] + 1
    print("Total Fresh:", total)
    return total

assert_equals(total_fresh(TEST_INPUT), 3)
total_fresh(INPUT)

assert_equals(all_fresh(TEST_INPUT), 14)
# all_fresh(INPUT)
# 350339340818552 - too high?