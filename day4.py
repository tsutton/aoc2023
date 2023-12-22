from collections import defaultdict

def example_input() -> list[str]:
    example = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines

def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day4.txt", 'r') as f:
        for line in f:
            lines.append(line.strip()) # skip trailing mewline

    return lines

def main():
    lines = real_input()
    # lines = example_input()

    parts = pt1(lines)
    print(parts)

    print(pt2(lines))

def parse_line(line: str) -> tuple[ set, set]:
    wins = set()
    ours = set()

    parts = line.split(":")
    line = parts[1].lstrip()
    winStr, ourStr = line.split("|")

    for s in winStr.strip().split(' '):
        if not s: continue
        wins.add(int(s))

    for s in ourStr.strip().split(' '):
        if not s: continue
        ours.add(int(s))

    return (wins, ours)

def pt1(lines: list[str]) -> int:
    tot = 0
    for line in lines:
        wins, ours = parse_line(line)
        l = wins.intersection(ours)
        if len(l) > 0:
            tot += 2** (len(l)-1)
    return tot

def pt2(lines: list[str]) -> int:

    # first figure out, for each game, how many wins that game has by itself
    # (not considering copies or anthing)

    winCounts = []

    for line in lines:
        wins, ours = parse_line(line)
        winCount = len(wins.intersection(ours))
        winCounts.append(winCount)

    counts = defaultdict(int)
    for i in range(len(winCounts)):
        # assume at the point we are at i, counts already tells us how many copies of it we have from prev ones

        # add the one original
        counts[i] += 1
        for j in range(i+1, i+winCounts[i]+1):
            counts[j] += counts[i]

    return sum(counts.values())


if __name__ == "__main__":
    main()

