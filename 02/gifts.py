from util import assert_equals, file_as_string

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def total_invalid(start, end):
    total = 0
    for i in range(start, end + 1):
        stringified = str(i)
        half_one = stringified[0:len(stringified) // 2]
        half_two = stringified[len(stringified) // 2:]
        if half_one == half_two:
            total += i

    return total

def sum_invalids(file):
    total = 0
    range_strings = file_as_string(file, joined=True).split(",")
    range_strings = [r.split("-") for r in range_strings]
    ranges = [(int(nums[0]), int(nums[1])) for nums in range_strings]

    for int_range in ranges:
        total += total_invalid(int_range[0], int_range[1])

    print("Total invalid:", total)
    return total


assert_equals(sum_invalids(TEST_INPUT), 1227775554)
sum_invalids(INPUT)