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

    example = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

    example = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
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
    # Strategy:
    # find the S
    # figure out what the S is
    # find the main loop, and stick it in a set
    # pick any outside starting point
    # awkward floodfill by halves

    width = len(lines[0])
    height = len(lines)
    s_row, s_col = (0, 0)
    for row_num, line in enumerate(lines):
        col_num = line.find("S")
        if col_num != -1:
            s_row, s_col = (row_num, col_num)
            break

    has_left = s_col > 0 and lines[s_row][s_col - 1] in ["-", "F", "L"]
    has_right = s_col + 1 < width and lines[s_row][s_col + 1] in ["-", "J", "7"]
    has_up = s_row > 0 and lines[s_row - 1][s_col] in ["|", "7", "F"]
    has_down = s_row + 1 < height and lines[s_row + 1][s_col] in ["|", "L", "J"]

    main_loop = set([(s_row, s_col)])
    main_loop_ordered = [(s_row, s_col)]
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

    s_actual = ""
    if has_left and has_up:
        s_actual = "J"
    elif has_left and has_down:
        s_actual = "7"
    elif has_left and has_right:
        s_actual = "-"
    elif has_right and has_up:
        s_actual = "L"
    elif has_right and has_down:
        s_actual = "F"
    elif has_up and has_down:
        s_actual = "|"

    lines[s_row] = lines[s_row].replace("S", s_actual)

    while (row, col) != (s_row, s_col):
        main_loop.add((row, col))
        main_loop_ordered.append((row, col))
        # print(f"currently at ({row}, {col}), char is {lines[row][col]}")
        possible_directions = deltas[lines[row][col]]
        next_direction = possible_directions[0]
        if possible_directions[0] == came_from:
            next_direction = possible_directions[1]
        row, col = (row + next_direction[0], col + next_direction[1])
        came_from = (-next_direction[0], -next_direction[1])

    # print(sorted(list(main_loop)))

    inside_outside_map = {}  # our flood-fill visited map
    # maps (coord, coord) = True: visited

    # assume something in the top row is not in the main loop
    # col = 0
    # while lines[col] in main_loop:
    #     col += 1

    # inside_outside_map = {}

    # queue = [(0.0, float(col))]

    queue = []
    for col in range(width):
        if lines[0][col] not in main_loop:
            queue.append((0, col))
        if lines[height - 1][col] not in main_loop:
            queue.append((height - 1, col))

    for row in range(height):
        if lines[row][0] not in main_loop:
            queue.append((row, 0))
        if lines[row][width - 1] not in main_loop:
            queue.append((row, width - 1))

    while len(queue) > 0:
        (row, col) = queue.pop()
        if row < 0 or row >= height:
            continue
        if col < 0 or col >= width:
            continue
        if (row, col) in main_loop:
            continue
        if (row, col) in inside_outside_map:
            continue
        inside_outside_map[(row, col)] = True
        # if we are on an integer point, we can always go half-step in any direction
        integer_row = row == int(row)
        integer_column = col == int(col)
        up = (row - 0.5, col)
        down = (row + 0.5, col)
        left = (row, col - 0.5)
        right = (row, col + 0.5)
        if integer_column and integer_row:
            for always in [up, down, left, right]:
                if always not in inside_outside_map and always not in main_loop:
                    queue.append(always)
        elif integer_column and not integer_row:
            # we are in between rows, but at an integer column
            # we can always go left and right
            for always in [left, right]:
                if always not in inside_outside_map and always not in main_loop:
                    queue.append(always)

            for sometimes in [up, down]:
                if sometimes not in main_loop and sometimes not in inside_outside_map:
                    queue.append(sometimes)

        elif integer_row:
            # we are in between columns, but at an integer row
            # we can always go up and down
            for always in [up, down]:
                if always not in inside_outside_map and always not in main_loop:
                    queue.append(always)

            for sometimes in [left, right]:
                if sometimes not in main_loop and sometimes not in inside_outside_map:
                    queue.append(sometimes)
        else:
            # this is the tricky one where we have to check if we are passing in between pipes

            # we can go UP to an integer row if up is not along the main path, that is, it's not in between something like:
            # -- ; F-, L-, LJ etc
            # we can check up and to the left to see if it connects right: F, -, L

            check_and_enqueues = []

            upleft_row, upleft_col = (up[0], up[1] - 0.5)
            if (
                upleft_row < 0
                or upleft_col < 0
                or (
                    (upleft_row, upleft_col) not in main_loop
                    or lines[int(upleft_row)][int(upleft_col)]
                    not in [
                        "F",
                        "-",
                        "L",
                    ]
                )
            ):
                check_and_enqueues.append(up)

            # for going down, check down_left
            downleft_row, downleft_col = (down[0], down[1] - 0.5)
            if (
                downleft_row < 0
                or downleft_row >= height
                or downleft_col >= width
                or (
                    (downleft_row, downleft_col) not in main_loop
                    or lines[int(downleft_row)][int(downleft_col)]
                    not in [
                        "F",
                        "-",
                        "L",
                    ]
                )
            ):
                check_and_enqueues.append(down)

            # for going left, check upleft also
            if (
                upleft_row < 0
                or upleft_col < 0
                or (
                    (upleft_row, upleft_col) not in main_loop
                    or lines[int(upleft_row)][int(upleft_col)]
                not in [
                    "|",
                    "F",
                    "7",
                ])
            ):
                check_and_enqueues.append(left)

            # for going right, check up right (could also check down right)
            downright_row, downright_col = (down[0], down[1] + 0.5)
            if (
                downright_row >= height
                or downright_col >= width
                or (
                    (downright_row, downright_col) not in main_loop

                    or lines[int(downright_row)][int(downright_col)]
                not in [
                    "|",
                    "J",
                    "L",
                ])
            ):
                check_and_enqueues.append(right)

            for q in check_and_enqueues:
                if q not in inside_outside_map and q not in main_loop:
                    queue.append(q)

    print(inside_outside_map[(28.5, 83.5)])

    integral_visited = list(
        filter(
            lambda x: x[0] == int(x[0]) and x[1] == int(x[1]),
            inside_outside_map.keys(),
        )
    )

    # print(debug_view(main_loop, integral_visited, height, width))
    visualized = debug_double_view(
        main_loop_ordered, list(inside_outside_map.keys()), height, width
    )
    # print(visualized)

    count = 0
    for j, line in enumerate(visualized.splitlines()):
        for i, c in enumerate(line):
            if i % 2 == 0 and j % 2 == 0 and c == ".":
                count += 1
    print(count)

    return width * height - len(integral_visited) - len(main_loop)


def debug_view(
    main_loop: set[tuple[int, int]],
    integral_visited: list[tuple[int, int]],
    height: int,
    width: int,
) -> str:
    new_grid = [["." for _ in range(width)] for _ in range(height)]
    for g in main_loop:
        new_grid[g[0]][g[1]] = "#"

    for g in integral_visited:
        new_grid[int(g[0])][int(g[1])] = "O"

    return "\n".join(["".join(l) for l in new_grid])


def debug_double_view(
    main_loop_ordered: list[tuple[int, int]],
    visited: list[tuple[float, float]],
    height: int,
    width: int,
) -> str:
    new_grid = [["." for _ in range(2 * width)] for _ in range(2 * height)]

    start = main_loop_ordered[0]
    new_grid[start[0] * 2][start[1] * 2] = "#"

    for j in range(1, len(main_loop_ordered)):
        previous_pipe = main_loop_ordered[j - 1]
        next_pipe = main_loop_ordered[j]
        new_grid[next_pipe[0] * 2][next_pipe[1] * 2] = "#"
        intermediate_row = previous_pipe[0] + next_pipe[0]
        intermediate_col = previous_pipe[1] + next_pipe[1]
        new_grid[intermediate_row][intermediate_col] = "#"

    for g in visited:
        new_grid[int(g[0] * 2)][int(g[1] * 2)] = "O"

    return "\n".join(["".join(l) for l in new_grid])


if __name__ == "__main__":
    main()
