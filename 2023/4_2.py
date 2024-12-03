import collections
from utils import read_input

example = read_input("./4_example.txt")
input = read_input("./4_input.txt")


def get_total_cards(input):
    won_cards_by_card_id = collections.defaultdict(int)

    for line in input:
        card, my_numbers = line.split("|")
        my_numbers = my_numbers.split()

        card_id, card_numbers = card.split(":")
        card_numbers = card_numbers.split()
        card_id = int(card_id.split()[1])

        won_cards_by_card_id[card_id] += 1

        winning_numbers = 0

        for number in card_numbers:
            if number in my_numbers:
                winning_numbers += 1

        for i in range(1, winning_numbers + 1):
            won_cards_by_card_id[card_id + i] += won_cards_by_card_id[card_id]

        winning_numbers = 0

    return sum(won_cards_by_card_id.values())


assert get_total_cards(example) == 30

print(f"solution: {get_total_cards(input)}")
