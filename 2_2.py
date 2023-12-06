from utils import read_input

example = read_input("./2_example.txt")
input = read_input("./2_input.txt")

def check_games(input, config):
    game_cubes_sum = 0
    for string in input:
        print('string', string)
        max_colors = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        game_string, colors = string.split(":")
        _, game_id = game_string.split()

        for all_colors in colors.split(";"):
            for value__color in all_colors.split(","):
                value, color = value__color.split()
            
                if int(value) > max_colors[color]:
                    max_colors[color] = int(value)

        cubes_power = 1
        for cube_power in max_colors.values():
            cubes_power *= cube_power
        game_cubes_sum += cubes_power
    
    return game_cubes_sum

CONFIG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

assert(check_games(example, CONFIG) == 2286)

print('solution', check_games(input, CONFIG))