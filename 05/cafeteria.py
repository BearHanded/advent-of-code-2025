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
        for (range_start, range_end) in fresh:
            if ingredient in range(range_start, range_end + 1):
                total += 1
                break
    print("Total Fresh:", total)
    return total


def merge_fresh(fresh):
    merging = True
    while merging:
        merging = False
        for a_idx, (a_start, a_end) in enumerate(fresh):
            for b_idx, (b_start, b_end) in enumerate(fresh[a_idx + 1:]):
                if b_start <= a_start <= b_end \
                        or b_start <= a_end <= b_end \
                        or a_start <= b_start <= a_end \
                        or a_start <= b_end <= a_end:
                    merging = True
                    fresh[a_idx] = (min(a_start, b_start), max(a_end, b_end))
                    fresh.pop(a_idx + b_idx + 1)
                    break
            if merging:
                break
    return fresh

def all_fresh(filename):
    lines = file_to_array(filename)
    fresh = [tuple(int(i) for i in endpoints.split("-")) for endpoints in lines[:lines.index("")]]
    fresh = merge_fresh(fresh)

    total = sum(end - start + 1 for start, end in fresh)
    print("Total Fresh:", total)
    return total

assert_equals(total_fresh(TEST_INPUT), 3)
total_fresh(INPUT)

assert_equals(all_fresh(TEST_INPUT), 14)
all_fresh(INPUT)
