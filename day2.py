from dataclasses import dataclass


def main():
    lines: list[str] = []
    with open("inputs/day2.txt", "r") as f:
        for line in f:
            lines.append(line)

    #     example =  """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    # """
    #     for line in example.splitlines():
    #         lines.append(line)

    print(sum(pt1(line) for line in lines))
    print(sum(pt2(line) for line in lines))


@dataclass
class Drawing:
    red: int
    blue: int
    green: int


def parse_drawing(drawing: str) -> Drawing:
    red = 0
    green = 0
    blue = 0

    parts = drawing.split(",")
    for part in parts:
        count, color = part.strip().split(" ")
        if color == "red":
            red = int(count)
        elif color == "blue":
            blue = int(count)
        elif color == "green":
            green = int(count)

    return Drawing(red=red, green=green, blue=blue)


# returns the game number if it possible for 12R, 13G, 14B
# or else 0
def pt1(line: str) -> int:
    line = line[5:]  # strip "Game "
    game_number_str, rest = line.split(":", 1)
    drawings = [parse_drawing(d) for d in rest.strip().split(";")]
    for d in drawings:
        if d.red > 12 or d.green > 13 or d.blue > 14:
            return 0
    return int(game_number_str)


# returns the game power of a given game
def pt2(line: str) -> int:
    line = line[5:]  # strip "Game "
    _, rest = line.split(":", 1)
    drawings = [parse_drawing(d) for d in rest.strip().split(";")]
    max_red_seen = 0
    max_green_seen = 0
    max_blue_seen = 0
    for d in drawings:
        max_red_seen = max(max_red_seen, d.red)
        max_green_seen = max(max_green_seen, d.green)
        max_blue_seen = max(max_blue_seen, d.blue)
    return max_red_seen * max_blue_seen * max_green_seen


if __name__ == "__main__":
    main()
