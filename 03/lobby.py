from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def max_value(battery_array, size):
    start_idx = 0
    total = 0
    for i in range(size):
        search_window = battery_array[start_idx:len(battery_array)-(size-i-1)]
        max_left = max(search_window)
        max_left_idx = search_window.index(max_left)
        start_idx += max_left_idx + 1
        total += 10**(size-i-1) * max_left
    return total

def sum_values(filename, size):
    total = 0
    batteries = [list(int(i) for i in row) for row in file_to_array(filename)]
    for battery in batteries:
        total += max_value(battery, size)

    print("Sum Values:", total)
    return total


assert_equals(sum_values(TEST_INPUT, 2), 357)
sum_values(INPUT, 2)

assert_equals(sum_values(TEST_INPUT, 12), 3121910778619)
sum_values(INPUT, 12)