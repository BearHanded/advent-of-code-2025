from util import assert_equals, file_to_array

TEST_INPUT = "test_input.txt"
INPUT = "input.txt"

def build_instruction_line(line):
    chunks = line.split(" ")
    lights = list(chunks.pop(0)[1:-1])
    joltages = [int(i) for i in chunks.pop(-1)[1:-1].split(",")]
    schematics = [[int(i) for i in s[1:-1].split(",")] for s in chunks]
    return lights, schematics, joltages

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
                print("Found in ", next_press)
                return next_press
            if toggled_str in checked:
                continue

            queue.append((toggled, next_press))
            checked[toggled_str] = next_press

    return None


def minimum_buttons(filename):
    instructions = [build_instruction_line(row) for row in file_to_array(filename)]

    presses = 0
    for instruction in instructions:
        goal, schematics, joltages = instruction
        presses += match_display(goal, schematics)
    print("Minimum presses:", presses)
    return presses

# Pt 1
assert_equals(press_button([".", ".", "#", "."], (1, 2)), [".", "#", ".", "."])
assert_equals(minimum_buttons(TEST_INPUT), 7)
minimum_buttons(INPUT)