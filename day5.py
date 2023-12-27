from dataclasses import dataclass

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
    with open("inputs/day5.txt", 'r') as f:
        for line in f:
            lines.append(line.strip()) # skip trailing mewline

    return lines

@dataclass
class MappingInteval:
    source_start: int
    dest_start: int
    len: int

class Mapping:
    # should contain a sorted list of (start, dest_start, len) pairs
    # so the exapmle
    # 50 98 2
    # 52 50 48
    mappings: list[MappingInteval]

    def __init__(self, intervals: list[MappingInteval] = []):
        self.mappings = sorted(intervals, key = lambda interval: interval.source_start)

    def add_interval(self, interval: MappingInteval):
        self.mappings.append(interval)
        self.mappings.sort(key = lambda interval: interval.source_start)

    def __str__(self):
        return "\n".join(("dst {}, src {}, len {}".format(interval.dest_start, interval.source_start, interval.len) for interval in self.mappings))

    def map_input(self, in_value: int) -> int:
        if not self.mappings or in_value < self.mappings[0].source_start:
            return in_value

        # TODO Binary Search
        i = 0
        while i < len(self.mappings) and self.mappings[i].source_start <= in_value:
            i +=1

        if i == 0:
            return in_value
        best_guess_interval = self.mappings[i-1]
        if in_value <= best_guess_interval.source_start + best_guess_interval.len - 1:
            return best_guess_interval.dest_start + (in_value - best_guess_interval.source_start)
        else:
            return in_value


def parse(lines: list[str]) -> tuple[list[int], list[Mapping]]:
    seeds: list[int] = list(map( int, lines[0][7:].split()))
    lines = lines[2:]

    mappings: list[Mapping] = []

    i = 0
    
    while i < len(lines):
        # skip the leading line like "seed-to-x mapping"
        i += 1
        mapping = Mapping()
        while i < len(lines) and lines[i] != '':
            dest_start, source_start, length = lines[i].split()
            mapping.add_interval(MappingInteval(source_start=int(source_start), dest_start=int(dest_start), len=int(length)))
            i += 1
        i += 1 # empty line
        mappings.append(mapping)
    return (seeds, mappings)

def main():
    lines = real_input()
    # lines = example_input()

    print(pt1(lines))

    #print(pt2(lines))

def pt1(lines: list[str]):
    seeds, mappings = parse(lines)
    mapped_values = seeds
    for mapping in mappings:
        mapped_values = list(map(mapping.map_input, mapped_values))

    return min(mapped_values)

if __name__ == "__main__":
    main()

