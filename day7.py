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


FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0


class Hand2:
    cards: list[int]  # card from 2 to 14

    def __init__(self, cards: list[int]):
        self.cards = cards

    @classmethod
    def from_string(cls, hand: str) -> Self:
        mapping = {str(i): i for i in range(2, 10)}
        mapping["T"] = 10
        mapping["J"] = 1
        mapping["Q"] = 11
        mapping["K"] = 12
        mapping["A"] = 13
        return Hand2(list(map(lambda s: mapping[s], hand)))

    def type_value(self):
        joker_count = self.cards.count(1)
        if joker_count == 0:
            return Hand(self.cards).type_value()

        d = {}
        for c in self.cards:
            if c == 1:
                continue
            d[c] = 1 if c not in d else d[c] + 1

        parts = list(d.values())
        parts.sort()

        if joker_count == 1:
            # four cards can be 1,1,1,1; 1,1,2; 1,3; 2,2; or 4;
            if parts == [1, 1, 1, 1]:
                return ONE_PAIR
            if parts == [1, 1, 2]:
                return max(TWO_PAIR, THREE_OF_A_KIND)
            if parts == [2, 2]:
                return FULL_HOUSE
            if parts == [1, 3]:
                return max(FULL_HOUSE, FOUR_OF_A_KIND)
            if parts == [4]:
                return FIVE_OF_A_KIND

        if joker_count == 2:
            # three cards can be [1,1,1], [1,2] or [3]
            if parts == [1, 1, 1]:
                return max(TWO_PAIR, THREE_OF_A_KIND)
            if parts == [1, 2]:
                return max(FOUR_OF_A_KIND, FULL_HOUSE)
            if parts == [3]:
                return FIVE_OF_A_KIND

        if joker_count == 3:
            if parts == [1, 1]:
                return FOUR_OF_A_KIND
            if parts == [2]:
                return FIVE_OF_A_KIND

        if joker_count == 4 or joker_count == 5:
            return FIVE_OF_A_KIND

        raise NotImplementedError(joker_count, parts)

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
    # list of (hand_value, bid)
    hands: list[tuple[list[int], int]] = []
    for line in lines:
        hand_s, bid_s = line.split()
        bid = int(bid_s)
        hand = Hand2.from_string(hand_s)
        hands.append((hand.comparison_key(), bid))
    hands.sort()

    answer = 0
    for i, (_, bid) in enumerate(hands):
        answer += (i + 1) * bid

    return answer


if __name__ == "__main__":
    main()
