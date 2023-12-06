def main():
    lines: List[str] = []
    with open("inputs/day1.txt", 'r') as f:
        for line in f:
            lines.append(line)

    return sum(pt1(line) for line in lines)

def pt1(line: str):
    first_digit = None
    for c in line:
        if c in '0123456789':
            first_digit = c
            break

    last_digit = None
    for c in reversed(line):
        if c in '0123456789':
            last_digit = c
            break

    return int(first_digit+last_digit)

if __name__ == "__main__":
    print(main())
