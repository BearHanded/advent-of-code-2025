from util import assert_equals, file_as_string

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

# Pt 1, string only appears 2x
def total_invalid_reflected(start, end):
    total = 0
    for i in range(start, end + 1):
        stringified = str(i)
        half_one = stringified[0:len(stringified) // 2]
        half_two = stringified[len(stringified) // 2:]
        if half_one == half_two:
            total += i

    return total

# Pt 2, string appears many times
def total_invalid(start, end):
    total = 0
    for i in range(start, end + 1):
        stringified = str(i)
        target_string = ""
        for c in stringified[:len(stringified) // 2]:
            target_string += c
            stripped = stringified.replace(target_string, "")
            if len(stripped) == 0:
                total += i
                print("MATCH", i)
                break

    return total

def build_ranges(filename):
    range_strings = file_as_string(filename, joined=True).split(",")
    range_strings = [r.split("-") for r in range_strings]
    ranges = [(int(nums[0]), int(nums[1])) for nums in range_strings]
    return ranges

def sum_invalids(file, reflection):
    ranges = build_ranges(file)
    total = 0
    for int_range in ranges:
        if reflection: # pt 1
            total += total_invalid_reflected(int_range[0], int_range[1])
        else: # pt 2
            total += total_invalid(int_range[0], int_range[1])

    print("Total invalid:", total)
    return total


assert_equals(sum_invalids(TEST_INPUT, True), 1227775554)
sum_invalids(INPUT, True)

assert_equals(sum_invalids(TEST_INPUT, False), 4174379265)
sum_invalids(INPUT, False)