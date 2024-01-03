from math import lcm


def example_input() -> list[str]:
    example = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day8.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines


def main():
    lines = real_input()
    # lines = example_input()

    # print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]) -> int:
    instructions = lines[0]

    graph = {}

    for line in lines[2:]:
        # 0123456789012345
        # AAA = (BBB, CCC)
        node = line[:3]
        left = line[7:10]
        right = line[12:15]
        graph[node] = (left, right)

    current_node = "AAA"
    step_count = 0
    while current_node != "ZZZ":
        instruction = instructions[step_count % len(instructions)]
        next_pair = graph[current_node]
        if instruction == "L":
            current_node = next_pair[0]
        else:
            current_node = next_pair[1]
        step_count += 1

    return step_count


def pt2(lines: list[str]) -> int:
    instructions = lines[0]

    graph = {}

    for line in lines[2:]:
        # 0123456789012345
        # AAA = (BBB, CCC)
        node = line[:3]
        left = line[7:10]
        right = line[12:15]
        graph[node] = (left, right)

    steps_to_end = []
    for start in graph.keys():
        if start[2] == "A":
            steps_to_end.append(find_steps_to_z(graph, instructions, start))

    return lcm(*steps_to_end)


def find_steps_to_z(
    graph: dict[str, tuple[str, str]], instructions: str, start: str
) -> int:
    current_node = start
    step_count = 0
    while current_node[2] != "Z":
        instruction = instructions[step_count % len(instructions)]
        next_pair = graph[current_node]
        if instruction == "L":
            current_node = next_pair[0]
        else:
            current_node = next_pair[1]
        step_count += 1
    return step_count


if __name__ == "__main__":
    main()
