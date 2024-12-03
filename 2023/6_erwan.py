from utils import read_input

input = read_input("6_input.txt")


def get_inputs(input):
    times, distances = input
    times = times.split(":")[1].split()
    distances = distances.split(":")[1].split()

    return int("".join(times)), int("".join(distances))


class Race:
    def __init__(self, max_time, record):
        self.max_time = max_time
        self.record = record
        self.boat_speed = 0
        self.seconds = 0
        self.distance = 0
        self.number_of_winning_seconds_to_hold = 0

    def hold_and_release(self, seconds):
        self.boat_speed += seconds
        self.seconds += seconds
        self.release()

    def release(self):
        self.distance = self.boat_speed * (self.max_time - self.seconds)

    def reset(self):
        self.boat_speed = 0
        self.seconds = 0
        self.distance = 0


def main():
    races = []

    max_time, record = get_inputs(input)
    races.append(Race(max_time, record))

    for race in races:
        for seconds_to_hold in range(1, race.max_time + 1):
            race.hold_and_release(seconds_to_hold)
            if race.distance > race.record:
                race.number_of_winning_seconds_to_hold += 1
            race.reset()

        print(race.number_of_winning_seconds_to_hold)


if __name__ == "__main__":
    main()
