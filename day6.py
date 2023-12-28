from math import sqrt, floor, ceil


def example_input() -> list[str]:
    example = """\
Time:      7  15   30
Distance:  9  40  200
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


# returns (min, max) of times that beat the record
# assumes that there are SOME times, if there are not it might return like (x, x-1)
def hold_times_to_win(race_time: int, record: int) -> tuple[int, int]:
    # formula: T = race time, i = held-down-time
    # (T-i) * i
    # solve T i - i^2 = x
    # i^2 - T i + x = 0
    # i = (T +- sqrt(T^2 - 4 x)) / 2
    min_exact = 0.5 * (race_time - sqrt(race_time**2 - 4 * record))
    max_exact = 0.5 * (race_time + sqrt(race_time**2 - 4 * record))
    # special case for integer roots
    if int(min_exact) * (race_time - int(min_exact)) == record:
        print("special case")
        return (int(min_exact) + 1, int(max_exact) - 1)
    else:
        return (ceil(min_exact), floor(max_exact))


def main():
    lines = real_input()
    # lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    time_strs = lines[0][len("Time:") :].strip().split(" ")
    times = [int(i) for i in time_strs if i]

    distance_strs = lines[1][len("Distance:") :].strip().split(" ")
    distances = [int(i) for i in distance_strs if i]

    answer = 1
    for i in range(len(times)):
        min_time, max_time = hold_times_to_win(times[i], distances[i])
        print(f"race {i} has ({min_time}, {max_time})")
        answer *= max(max_time - min_time + 1, 0)

    return answer


def pt2(lines: list[str]):
    time = int("".join(lines[0][len("Time:") :].strip().split(" ")))
    distance = int("".join(lines[1][len("Distance:") :].strip().split(" ")))

    print(time, distance)

    min_time, max_time = hold_times_to_win(time, distance)
    print(f"race has ({min_time}, {max_time})")
    return max(max_time - min_time + 1, 0)


if __name__ == "__main__":
    main()
