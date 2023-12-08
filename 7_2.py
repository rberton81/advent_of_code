import collections
from utils import read_input


class Type:
    FiK = 6  # "Five Of A Kind"
    FoK = 5  # "Four Of A Kind"
    FH = 4  # "Full House"
    TK = 3  # "Three Of A Kind"
    TP = 2  # "Two Pairs"
    OP = 1  # "One Pair"
    HC = 0  # "High Card"


TO_BASE_13 = {
    "J": 1,
    **{f"{i}": i for i in range(2, 10)},
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


class Hand:
    def __init__(self, hand, bid):
        self._hand = hand
        self.value = Hand.get_value(hand)
        self.bid = bid
        hand_dict = Hand.to_dict(hand)
        self.type = Hand.get_type(hand_dict, hand)

    @classmethod
    def get_type(cls, hand_dict, hand):
        joker_count = 0
        if "J" in hand_dict:
            joker_count = hand_dict["J"]
            del hand_dict["J"]

        if joker_count == 5:
            return Type.FiK

        if joker_count:
            max_count = max(list(hand_dict.values()))

            for card, count in hand_dict.items():
                if count == max_count and card != "J":
                    hand_dict[card] += joker_count
                    break

        unique_cards_count = len(set(hand_dict.keys()))
        if unique_cards_count == 1:
            return Type.FiK
        elif unique_cards_count == 2:
            for card, count in hand_dict.items():
                if count in [1, 4]:
                    return Type.FoK
            return Type.FH
        elif unique_cards_count == 5:
            return Type.HC
        elif unique_cards_count == 4:
            return Type.OP
        elif unique_cards_count == 3:
            for card, count in hand_dict.items():
                if count == 3:
                    return Type.TK
            return Type.TP

    @classmethod
    def get_value(cls, hand):
        value = 0

        power = len(hand) - 1
        base = 13
        for card in hand:
            value += TO_BASE_13[card] * base**power
            power -= 1
        return value

    @classmethod
    def to_dict(cls, hand):
        hand_dict = collections.defaultdict(int)
        for char in hand:
            hand_dict[char] += 1
        return hand_dict


def get_solution(input):
    hand_by_type = collections.defaultdict(list)
    for hand__bid in input:
        hand, bid = hand__bid.split()
        _hand = Hand(hand, int(bid))
        hand_by_type[_hand.type].append(_hand)

    rank = 1
    bids_sum = 0

    for card_type in range(0, Type.FiK + 1):
        hands = hand_by_type[card_type] or []
        hands.sort(key=lambda hand: hand.value)
        for hand in hands:
            bids_sum += hand.bid * rank
            rank += 1

    return bids_sum


example = read_input("7_example.txt")
assert get_solution(example) == 5905

input = read_input("7_input.txt")
solution = get_solution(input)
print("solution", solution)
