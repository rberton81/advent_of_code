from utils import read_input


example = read_input("./4_example.txt")
input = read_input("./4_input.txt")


def get_total_points(input):
    total_points = 0
    for line in input:
        card, my_numbers = line.split("|")
        my_numbers = my_numbers.split()

        _, card_numbers = card.split(":")
        card_numbers = card_numbers.split()

        winning_numbers = 0

        for number in card_numbers:
            if number in my_numbers:
                winning_numbers += 1

        points = 0
        if winning_numbers:
            points = 2 ** (winning_numbers - 1)

        # print('points', points)
        total_points += points

    return total_points


assert get_total_points(example) == 13

print(f"solution: {get_total_points(input)}")
