def example_input() -> list[str]:
    example = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day9.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines


def main():
    lines = real_input()
    # lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    sequences = [[int(x) for x in line.split()] for line in lines]
    return sum([predict_next(sequence) for sequence in sequences])


def predict_next(sequence: list[int]) -> int:
    differences: list[list[int]] = [sequence]
    while True:
        next_difference = []
        for i in range(len(differences[-1]) - 1):
            next_difference.append(differences[-1][i + 1] - differences[-1][i])
        differences.append(next_difference)
        if not any(next_difference):
            break

    differences[-1].append(0)

    for i in range(len(differences) - 1):
        differences[-i - 2].append(differences[-i - 1][-1] + differences[-i - 2][-1])
    return differences[0][-1]


def predict_previous(sequence: list[int]) -> int:
    differences = [sequence]
    while True:
        next_difference = []
        for i in range(len(differences[-1]) - 1):
            next_difference.append(differences[-1][i + 1] - differences[-1][i])
        differences.append(next_difference)
        if not any(next_difference):
            break
    differences[-1].append(0)

    for i in range(len(differences) - 1):
        differences[-i - 2] = [
            differences[-i - 2][0] - differences[-i - 1][0]
        ] + differences[-i - 2]
    return differences[0][0]


def pt2(lines: list[str]):
    sequences = [[int(x) for x in line.split()] for line in lines]
    print([predict_previous(sequence) for sequence in sequences])
    return sum([predict_previous(sequence) for sequence in sequences])


if __name__ == "__main__":
    main()
