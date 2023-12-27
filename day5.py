from dataclasses import dataclass
from typing import Self


def example_input() -> list[str]:
    example = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day5.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines


@dataclass
class Interval:
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length - 1

    def overlap(self, other) -> Self | None:
        lower_start, higher_start = self, other
        if lower_start.start > higher_start.start:
            lower_start, higher_start = higher_start, lower_start

        if lower_start.end < higher_start.start:
            return None

        return Interval(
            start=higher_start.start,
            length=min(higher_start.end, lower_start.end) - higher_start.start + 1,
        )


@dataclass
class MappingInteval:
    source_start: int
    dest_start: int
    length: int

    def map_value(self, input_value: int) -> int:
        if (
            input_value < self.source_start
            or input_value > self.source_start + self.length - 1
        ):
            return input_value
        else:
            return self.dest_start + (input_value - self.source_start)

    def source_interval(self) -> Interval:
        return Interval(start=self.source_start, length=self.length)

    def map_interval(self, interval: Interval) -> list[Interval]:
        overlap = interval.overlap(self.source_interval())
        if overlap is None:
            return [interval]

        ret = []
        if overlap.start > interval.start:
            ret.append(
                Interval(
                    start=interval.start, length=overlap.start - interval.start + 1
                )
            )
        ret.append(
            Interval(
                start=overlap.start + (self.dest_start - self.source_start),
                length=overlap.length,
            )
        )
        if overlap.end < interval.end:
            ret.append(
                Interval(start=overlap.end + 1, length=interval.end - overlap.end)
            )

        return ret


class Mapping:
    # Contains a sorted list of (start, dest_start, len) pairs
    # If we had a binary tree or some kind other implementation of a Sorted list with log(n) insert while maintaining
    # order, that would be better
    intervals: list[MappingInteval]

    def __init__(self, intervals: list[MappingInteval] = []):
        self.intervals = sorted(intervals, key=lambda interval: interval.source_start)

    def add_interval(self, interval: MappingInteval):
        self.intervals.append(interval)
        self.intervals.sort(key=lambda interval: interval.source_start)

    def __str__(self):
        return "\n".join(
            (
                "dst {}, src {}, len {}".format(
                    interval.dest_start, interval.source_start, interval.length
                )
                for interval in self.intervals
            )
        )

    def map_input(self, in_value: int) -> int:
        if not self.intervals or in_value < self.intervals[0].source_start:
            return in_value

        # TODO Binary Search
        # Could use https://docs.python.org/3/library/bisect.html
        i = 0
        while i < len(self.intervals) and self.intervals[i].source_start <= in_value:
            i += 1

        if i == 0:
            return in_value
        best_guess_interval = self.intervals[i - 1]
        return best_guess_interval.map_value(in_value)

    def map_interval(self, interval: Interval) -> list[Interval]:
        i = 0
        while (
            i < len(self.intervals) and self.intervals[i].source_start <= interval.start
        ):
            i += 1

        # now self.mappings[i-1] is the only mapping interval that *might* contain interval_start

        j = i
        while (
            j < len(self.intervals)
            and self.intervals[j].source_start <= interval.start + interval.length - 1
        ):
            j += 1

        # now self.mappings[j-1] is the only mapping interval that *might* contain interval_end

        relevant_intervals = self.intervals[max(i - 1, 0) : j]
        # add a fake mapping interval with no-op for convenience/uniformity when i == 0
        if i == 0:
            relevant_intervals = [
                MappingInteval(
                    source_start=interval.start,
                    dest_start=interval.start,
                    length=self.intervals[0].source_start - interval.start,
                )
            ] + relevant_intervals

        # for each relevant interval, map from max(start of that interval, start of input) to min(start of the next interval - 1, end of input)
        ret = []
        for k in range(len(relevant_intervals)):
            relevant_interval = relevant_intervals[k]
            start = max(interval.start, relevant_interval.source_start)
            end = interval.end
            if k + 1 < len(relevant_intervals):
                end = min(end, relevant_intervals[k + 1].source_start - 1)
            ret += relevant_intervals[k].map_interval(
                Interval(start=start, length=end - start + 1)
            )

        return ret


def parse_seeds_part_1(seed_line: str) -> list[int]:
    return list(map(int, seed_line[7:].split()))


def parse_seeds_part_2(seed_line: str) -> list[Interval]:
    seeds: list[Interval] = []

    parts = seed_line[7:].split()
    for i in range(0, len(parts), 2):
        seeds.append(Interval(start=int(parts[i]), length=int(parts[i + 1])))

    return seeds


def parse_mappings(lines: list[str]) -> list[Mapping]:
    i = 0
    mappings = []
    while i < len(lines):
        # skip the leading line like "seed-to-x mapping"
        i += 1
        mapping = Mapping()
        while i < len(lines) and lines[i] != "":
            dest_start, source_start, length = lines[i].split()
            mapping.add_interval(
                MappingInteval(
                    source_start=int(source_start),
                    dest_start=int(dest_start),
                    length=int(length),
                )
            )
            i += 1
        i += 1  # empty line
        mappings.append(mapping)
    return mappings


def main():
    lines = real_input()
    # lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    seeds = parse_seeds_part_1(lines[0])
    mappings = parse_mappings(lines[2:])

    mapped_values = seeds
    for mapping in mappings:
        mapped_values = list(map(mapping.map_input, mapped_values))

    return min(mapped_values)


def pt2(lines: list[str]) -> int:
    seeds = parse_seeds_part_2(lines[0])
    mappings = parse_mappings(lines[2:])

    mapped_values = seeds
    for mapping in mappings:
        mapped_values = sum(map(mapping.map_interval, mapped_values), [])
    return min(map(lambda interval: interval.start, mapped_values))


if __name__ == "__main__":
    main()
