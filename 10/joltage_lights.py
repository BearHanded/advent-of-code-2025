from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def build_instruction_line(line):
    chunks = line.split(" ")
    lights = list(chunks.pop(0)[1:-1])
    joltages = tuple(int(i) for i in chunks.pop(-1)[1:-1].split(","))
    schematics = [[int(i) for i in s[1:-1].split(",")] for s in chunks]
    return lights, schematics, joltages


# Part 1
def press_button(display, button):
    out = []
    for idx, cell in enumerate(display):
        out.append(flip(cell) if idx in button else cell)
    return out

def flip(display_cell):
    return "#" if display_cell == "." else "."


def match_display(goal, schematics):
    checked = dict()
    checked["".join(goal)] = 0

    queue = [(["." for _ in goal], 0)]
    while len(queue) > 0:
        current_state, presses = queue.pop(0)
        next_press = presses + 1

        # Todo press button
        for button in schematics:
            toggled = press_button(current_state, button)
            toggled_str = " ".join(toggled)
            if toggled == goal:
                return next_press
            if toggled_str in checked:
                continue

            queue.append((toggled, next_press))
            checked[toggled_str] = next_press

    return None

def minimum_startup_buttons(filename):
    instructions = [build_instruction_line(row) for row in file_to_array(filename)]

    presses = 0
    for instruction in instructions:
        goal, schematics, joltages = instruction
        presses += match_display(goal, schematics)
    print("Minimum presses:", presses)
    return presses

# Part 2
def press_button_joltage(joltage_state, button):
    out = list()
    for idx, cell in enumerate(joltage_state):
        out.append(cell + 1 if idx in button else cell)
    return tuple(out)

def match_joltage(joltage_goal, schematics):
    checked = dict()
    zero_joltage = tuple(list([0] * len(joltage_goal)))
    checked[zero_joltage] = 0

    # print(checked)
    queue = [(zero_joltage, 0)]
    while len(queue) > 0:
        # print(queue)
        # print(checked)
        current_state, presses = queue.pop(0)
        next_press = presses + 1

        # Todo press button
        for button in schematics:
            new_joltages = press_button_joltage(current_state, button)
            # print(current_state)
            # print(button, new_joltages)
            if new_joltages == joltage_goal:
                print("Matched joltage:", next_press)
                return next_press
            overflow = False

            if new_joltages in checked:
                continue
            for idx, i in enumerate(new_joltages):
                if i > joltage_goal[idx]:
                    overflow = True
                    break

            if overflow:
                continue

            queue.append((new_joltages, next_press))
            checked[new_joltages] = next_press
    return None

def minimum_joltage_buttons(filename):
    instructions = [build_instruction_line(row) for row in file_to_array(filename)]

    presses = 0
    for instruction in instructions:
        goal, schematics, joltages = instruction
        presses += match_joltage(joltages, schematics)
    print("Minimum presses:", presses)
    return presses

# Pt 1
assert_equals(press_button([".", ".", "#", "."], (1, 2)), [".", "#", ".", "."])
assert_equals(minimum_startup_buttons(TEST_INPUT), 7)
minimum_startup_buttons(INPUT)

assert_equals(press_button_joltage((0, 1, 2, 3), (1, 2)), (0, 2, 3, 3))
assert_equals(minimum_joltage_buttons(TEST_INPUT), 33)
minimum_joltage_buttons(INPUT)