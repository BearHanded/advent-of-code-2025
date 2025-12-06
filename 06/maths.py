import operator
from functools import reduce

from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def do_worksheet(filename):
    total = 0
    worksheet = [line.split() for line in file_to_array(filename)]
    rotated = list(zip(*worksheet[::1]))
    for row in rotated:
        op = row[-1]
        vals = [int(i) for i in row[:-1]]
        if op == "+":
            total += sum(vals)
        else:
            total += reduce(operator.mul, vals, 1)
    print("Maths:", total)
    return total

def do_worksheet_better(filename):
    total = 0
    worksheet = file_to_array(filename)
    rotated = list(zip(*worksheet[::-1]))
    mirrored = [list(reversed(row)) for row in reversed(rotated)]
    values = []
    while len(mirrored) > 0:
        target = mirrored.pop(0)
        number_string = ''.join(target[:-1]).strip()
        if not number_string.isdigit():
            continue
        values.append(int(number_string))
        op = target[-1]
        if op == "+":
            total += sum(values)
            values = []
        elif op == "*":
            total += reduce(operator.mul, values, 1)
            values = []

    print("Maths:", total)
    return total

# Pt 1
assert_equals(do_worksheet(TEST_INPUT), 4277556)
do_worksheet(INPUT)

# Pt 2
assert_equals(do_worksheet_better(TEST_INPUT), 3263827)
do_worksheet_better(INPUT)
# NOTE: IDE TRIMMING WHITE SPACE ON INPUT. ADD SPACES BEFORE RUNNING