from utils import read_input

def get_seeds_and_ratios(input):
    sections = [section.strip() for section in input.strip().split('\n\n')]
    seeds_line = sections[0].split(': ')[1]
    seeds = list(map(int, seeds_line.split()))

    ratios = {}

    for section in sections[1:]:
        lines = section.split('\n')
        key = lines[0]

        map_data = [[int(value) for value in line.split()] for line in lines[1:]]
        
        ratios[key] = map_data

    print("seeds:", seeds)
    print("ratios:", ratios)

    return seeds, ratios

def get_min_location(input):
    seeds, transaction_name__ratios = get_seeds_and_ratios(input)
    # initial = [i for i in range(0, 100)] ##TODO only add given seeds!
    initial = [i for i in range(0, max(seeds))]
    # converted = [i for i in range(0, 100)]
    converted = [i for i in range(0, max(seeds))]

    for transaction_name, ratios in transaction_name__ratios.items():
        print('_______________________________')
        print(f'transaction {transaction_name}')

        for ratio in ratios:
            destination, source, _range = ratio
            print(f"config: dest={destination} source={source} range={_range}")

            for i in range(_range):
                # print(source+i, '->', destination+i)
                try:
                    index = initial.index(source+i) ##TODO that wont work...
                    converted[index] = destination+i
                    print(f"source = {source+i}, index= {index}, destination={destination+i}")
                    # import pdb; pdb.set_trace()
                    # print('foo')
                except Exception as err:
                    print('error')
                    import pdb; pdb.set_trace()
                    print('error')


                # converted[source+i] = destination+i

            # import pdb; pdb.set_trace()
            print('converted after')
            for i in range(len(converted)):
                print(f'index = {i} -> {converted[i]}')

        initial = converted.copy()
        # print(f'end transaction {transaction_name}')

        # for seed in seeds:
        #     print(f"seed {seed} -> {converted[seed]}")


    for seed in seeds:
        print(f"seed {seed} -> {converted[seed]}")

    min_location = min([converted[seed] for seed in seeds])
    print(f"location min : {min_location}")
    return min_location

# example = read_input("5_example.txt", by_line=False, in_one_line=True)
# assert(get_min_location(example) == 35)

input = read_input("./5_input.txt", by_line=False, in_one_line=True)
print('solution', get_min_location(input))

