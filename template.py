def example_input() -> list[str]:
    example = """\
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day6.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines

def main():
    # lines = real_input()
    lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    pass

def pt2(lines: list[str]):
    pass


if __name__ == "__main__":
    main()
