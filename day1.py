def main():
    lines: List[str] = []
    with open("inputs/day1.txt", 'r') as f:
        for line in f:
            lines.append(line)

    print(sum(pt1(line) for line in lines))
    print(sum(pt2(line) for line in lines))

def pt1(line: str):
    first_digit = None
    for c in line:
        if c.isnumeric():
            first_digit = c
            break

    last_digit = None
    for c in reversed(line):
        if c.isnumeric():
            last_digit = c
            break

    return int(first_digit+last_digit)

def pt2(line: str):
    first_digit = 0
    for idx in range(0, len(line)):
        val = number_at_start(line[idx:])
        if val is not None:
            first_digit = val
            break

    last_digit = 0
    for idx in range(len(line)-1, -1, -1):
        # print(f"checking {line[idx:]}")
        val = number_at_start(line[idx:])
        if val is not None:
            last_digit = val
            break

    return 10*first_digit+last_digit

def number_at_start(s: str) -> int | None:
    mapping: dict[str, int] = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight':8,
        'nine': 9,
    }
    if s[0].isnumeric():
        return int(s[0])
    for k, v in mapping.items():
        if s.startswith(k):
            return v
    return None

if __name__ == "__main__":
    main()
