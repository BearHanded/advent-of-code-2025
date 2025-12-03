from util import assert_equals, file_as_string, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def max_value(battery_array):
    max_left_idx = battery_array[:-1].index(max(battery_array[:-1]))
    max_right = max(battery_array[max_left_idx+1:])
    return battery_array[max_left_idx] * 10 + max_right

def sum_values(filename):
    total = 0
    batteries = [list(int(i) for i in row) for row in file_to_array(filename)]
    for battery in batteries:
        total += max_value(battery)

    print("Sum Values:", total)
    return total

assert_equals(sum_values(TEST_INPUT), 357)
sum_values(INPUT)
