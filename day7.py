from typing import Self


def example_input() -> list[str]:
    example = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

    lines: list[str] = []
    for line in example.splitlines():
        lines.append(line)
    return lines


class Hand:
    cards: list[int]  # card from 2 to 14

    def __init__(self, cards: list[int]):
        self.cards = cards

    @classmethod
    def from_string(cls, hand: str) -> Self:
        mapping = {str(i): i for i in range(2, 10)}
        mapping["T"] = 10
        mapping["J"] = 11
        mapping["Q"] = 12
        mapping["K"] = 13
        mapping["A"] = 14
        return Hand(list(map(lambda s: mapping[s], hand)))

    def type_value(self):
        d = {}
        for c in self.cards:
            d[c] = 1 if c not in d else d[c] + 1
        # 5-of-a-kind
        if len(d) == 1:
            return 6
        # full house or 4 of a kind
        if len(d) == 2:
            if 4 in d.values():
                return 5
            else:
                return 4
        # 3-of-a-kind or 2 pair
        if len(d) == 3:
            if 3 in d.values():
                return 3
            else:
                return 2
        if len(d) == 4:
            return 1
        return 0

    def comparison_key(self):
        tv = self.type_value()
        return [tv] + self.cards


def real_input() -> list[str]:
    lines: list[str] = []
    with open("inputs/day7.txt", "r") as f:
        for line in f:
            lines.append(line.strip())  # skip trailing mewline

    return lines


def main():
    lines = real_input()
    # lines = example_input()

    print("part 1 answer: ", pt1(lines))

    print("part 2 answer: ", pt2(lines))


def pt1(lines: list[str]):
    # list of (hand_value, bid)
    hands: list[tuple[list[int], int]] = []
    for line in lines:
        hand_s, bid_s = line.split()
        bid = int(bid_s)
        hand = Hand.from_string(hand_s)
        hands.append((hand.comparison_key(), bid))
    hands.sort()

    answer = 0
    for i, (_, bid) in enumerate(hands):
        answer += (i + 1) * bid

    return answer


def pt2(lines: list[str]):
    pass


if __name__ == "__main__":
    main()
