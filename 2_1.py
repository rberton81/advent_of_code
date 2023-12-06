from utils import read_input

example = read_input("./2_example.txt")
input = read_input("./2_input.txt")

def check_games(input, config):
    game_ids_sum = 0
    for string in input:
        game_is_valid = True

        game_string, colors = string.split(":")
        _, game_id = game_string.split()

        for all_colors in colors.split(";"):
            if not game_is_valid:
                break
            for value__color in all_colors.split(","):
                value, color = value__color.split()

                if int(value) > config[color]:
                    game_is_valid = False
        
        if game_is_valid:
            game_ids_sum += int(game_id)

    return game_ids_sum

CONFIG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

assert(check_games(example, CONFIG) == 8)

print('solution', check_games(input, CONFIG))