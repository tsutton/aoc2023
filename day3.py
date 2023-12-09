def example_input() -> list[str]:
    example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines

def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day3.txt", 'r') as f:
        for line in f:
            lines.append(line.strip()) # skip trailing mewline

    return lines

def main():
    lines = real_input()
    # lines = example_input()

    parts = pt1(lines)
    print(parts)
    print(sum(parts))
    pt2(lines)
    #print(sum(pt2(line) for line in lines))

# returns list of pairs (start, end) such that line[start:end] are the numbers in the line
def number_locations(line: str) -> list[tuple[int,int]]:
    locations = []
    char_idx = 0

    while char_idx <= len(line):
        # skip until we find a number
        while char_idx < len(line) and not line[char_idx].isnumeric():
            char_idx += 1
        if char_idx == len(line):
            break

        # go until we find the end of the number
        number_start = char_idx
        while char_idx < len(line) and line[char_idx].isnumeric():
            char_idx += 1

        locations.append((number_start,char_idx))

    return locations

def has_adjacent_symbol(grid: list[str], line: int, number_location: tuple[int,int]) -> bool:
    # print(f"checking {line=} and loc {number_location=}")
    for line_number in range(line-1, line+2):
        for col_number in range(number_location[0]-1, number_location[1]+1):
            # print(f"checking({line_number, col_number})")
            if line_number < 0 or line_number >= len(grid):
                # print("skipping due to line out of bounds")
                continue
            if col_number < 0 or col_number >= len(grid[line_number]):
                # print("skipping due to col out of bounds")
                continue
            c = grid[line_number][col_number]
            if not c.isnumeric() and c != '.':
                return True

    return False

# returns the list of engine parts from the schematic
def pt1(lines: list[str]) -> list[int]:
    engine_parts = []
    for i, line in enumerate(lines):
        locations = number_locations(line)
        for location in locations:
            if has_adjacent_symbol(lines, i, location):
                engine_parts.append(int(line[location[0]:location[1]]))

    return engine_parts

def adjacent_stars(grid: list[str], line: int, number_location: tuple[int,int]) -> list[tuple[int,int]]:
    stars = []
    for line_number in range(line-1, line+2):
        for col_number in range(number_location[0]-1, number_location[1]+1):
            # print(f"checking({line_number, col_number})")
            if line_number < 0 or line_number >= len(grid):
                # print("skipping due to line out of bounds")
                continue
            if col_number < 0 or col_number >= len(grid[line_number]):
                # print("skipping due to col out of bounds")
                continue
            if grid[line_number][col_number] == '*':
                stars.append((line_number,col_number))
    return stars

# returns the list of engine parts from the schematic
def pt2(lines: list[str]) :
    stars: dict[tuple[int,int],list[int]] = {}
    for i, line in enumerate(lines):
        locations = number_locations(line)
        for location in locations:
            for star in adjacent_stars(lines, i, location):
                if star not in stars:
                    stars[star] = [int(lines[i][location[0]:location[1]])]
                else:
                    stars[star].append(int(lines[i][location[0]:location[1]]))

    print(stars)

    answer = 0
    for star, parts in stars.items():
        if len(parts) == 2:
            answer += parts[0] * parts[1]

    print(answer)


if __name__ == "__main__":
    main()

