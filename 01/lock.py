from util import assert_equals, file_to_array

TEST_INPUT = "01/test_input.txt"
INPUT = "01/input.txt"

# Number of times pointing at 0
def spin_lock(file):
    instructions = [(-1 if instr[0] == "L" else 1) * int(instr[1:]) for instr in file_to_array(file)]

    matches = 0
    position = 50
    for instruction in instructions:
        position += instruction
        if position % 100 == 0:
            matches += 1

    print("Total zeroed:", matches)
    return matches


def zeroes_between(instruction, position):
    # normalize to a positive path, with start as distance from next threshold
    # we can treat the end position as inclusive
    start = position if instruction > 0 else 100 - position
    end = start + abs(instruction)
    passing_zero = (end // 100) - (start // 100)

    return passing_zero

# Number of times passing through 0
def tick_lock(file):
    instructions = [(-1 if instr[0] == "L" else 1) * int(instr[1:]) for instr in file_to_array(file)]

    matches = 0
    position = 50
    for instruction in instructions:
        new_position = position + instruction
        matches += zeroes_between(instruction, position)
        position = new_position % 100

    print("Total passing zero:", matches)
    return matches

# Pt 1
assert_equals(spin_lock(TEST_INPUT), 3)
spin_lock(INPUT)

# Pt 2
assert_equals(tick_lock(TEST_INPUT), 6)
tick_lock(INPUT)