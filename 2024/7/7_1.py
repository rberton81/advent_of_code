import collections
from utils.utils import read_input


class CannotReachTargetException(Exception):
    pass


class Operators:
    MULTIPLY = "*"
    ADD = "+"


def add_or_multiply(
    target, current_computation, numbers, operator, only_multiply=False, only_add=False
):
    if numbers:
        number = numbers.popleft()
        if number == 1 and only_multiply:  # +1 > *1
            only_multiply = False

        if operator == Operators.ADD:
            current_computation += number
            only_multiply = False
        elif operator == Operators.MULTIPLY:
            current_computation *= number
            only_add = False
        return add_or_multiply(
            target,
            current_computation,
            numbers.copy(),
            Operators.MULTIPLY,
            only_multiply=only_multiply,
        ) or add_or_multiply(
            target, current_computation, numbers, Operators.ADD, only_add=only_add
        )
    else:
        if current_computation == target:
            return True
        elif only_multiply and current_computation < target:
            raise CannotReachTargetException()
        elif only_add and current_computation > target:
            raise CannotReachTargetException()
        else:
            return False


def solution(input):
    reached_targets_sum = 0
    for line in read_input(input):
        target, numbers = line.split(":")
        target = int(target)
        numbers = collections.deque([int(number) for number in numbers.split()])

        current_computation = numbers.popleft()
        try:
            if add_or_multiply(
                target,
                current_computation,
                numbers.copy(),
                Operators.MULTIPLY,
                only_multiply=True,
            ) or add_or_multiply(
                target, current_computation, numbers, Operators.ADD, only_add=True
            ):
                reached_targets_sum += target
        except CannotReachTargetException:
            continue
    return reached_targets_sum


assert solution("example.txt") == 3749
print("solution: ", solution("input.txt"))
