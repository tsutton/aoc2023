def example_input() -> list[str]:
    example = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""

    example = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


# everything is GRID[row][col] starting from (0,0)
deltas = {
    "|": [(-1, 0), (+1, 0)],
    "-": [(0, -1), (0, +1)],
    "L": [(-1, 0), (0, +1)],
    "J": [(-1, 0), [0, -1]],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    ".": [],
    "S": [],
}


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day10.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines


def main():
    lines = real_input()
    # lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    # Strategy:
    # find the S
    # figure out what the S is
    # Start going!
    # when we get back, answer is length / 2

    width = len(lines[0])
    s_row, s_col = (0, 0)
    for row_num, line in enumerate(lines):
        col_num = line.find("S")
        if col_num != -1:
            s_row, s_col = (row_num, col_num)
            break

    has_left = s_col > 0 and lines[s_row][s_col - 1] in ["-", "F", "L"]
    has_right = s_col + 1 < width and lines[s_row][s_col + 1] in ["-", "J", "7"]
    has_up = s_row > 0 and lines[s_row - 1][s_col] in ["|", "7", "F"]

    loop_length = 1
    row = s_row
    col = s_col
    came_from = (0, 0)  # from current (row, col)  to previous one
    if has_left:
        col = s_col - 1
        came_from = (0, +1)
    elif has_right:
        col = s_col + 1
        came_from = (0, -1)
    elif has_up:
        row = s_row - 1
        came_from = (1, 0)
    # at least two of those must be true, so only have to check three of them.

    while (row, col) != (s_row, s_col):
        # print(f"currently at ({row}, {col}), char is {lines[row][col]}")
        possible_directions = deltas[lines[row][col]]
        next_direction = possible_directions[0]
        if possible_directions[0] == came_from:
            next_direction = possible_directions[1]
        row, col = (row + next_direction[0], col + next_direction[1])
        loop_length += 1
        came_from = (-next_direction[0], -next_direction[1])

    return loop_length / 2


def pt2(lines: list[str]):
    pass


if __name__ == "__main__":
    main()
