import collections
from utils.utils import read_input


class Operators:
    MULTIPLY = "*"
    ADD = "+"
    CONCAT = "||"


def concat_multiply_or_add(target, current_computation, numbers, operator):
    if numbers:
        number = numbers.popleft()
        if operator == Operators.CONCAT:
            current_computation = int(f"{current_computation}{number}")
        elif operator == Operators.MULTIPLY:
            current_computation *= number
        elif operator == Operators.ADD:
            current_computation += number

        if current_computation > target:
            return False

        return (
            concat_multiply_or_add(
                target, current_computation, numbers.copy(), Operators.CONCAT
            )
            or concat_multiply_or_add(
                target, current_computation, numbers.copy(), Operators.MULTIPLY
            )
            or concat_multiply_or_add(
                target, current_computation, numbers, Operators.ADD
            )
        )
    else:
        if current_computation == target:
            return True
        else:
            return False


def solution(input):
    reached_targets_sum = 0
    for line in read_input(input):
        target, numbers = line.split(":")
        target = int(target)
        numbers = collections.deque([int(number) for number in numbers.split()])

        full_concat = int("".join([str(number) for number in numbers]))
        full_sum = sum(numbers)
        if full_concat <= target:
            if full_concat == target:
                reached_targets_sum += target
            continue
        elif full_sum >= target:
            if full_sum == target:
                reached_targets_sum += target
            continue
        else:
            current_computation = numbers.popleft()
            if (
                concat_multiply_or_add(
                    target, current_computation, numbers.copy(), Operators.CONCAT
                )
                or concat_multiply_or_add(
                    target, current_computation, numbers.copy(), Operators.MULTIPLY
                )
                or concat_multiply_or_add(
                    target, current_computation, numbers, Operators.ADD
                )
            ):
                reached_targets_sum += target
    return reached_targets_sum


assert solution("example.txt") == 11387
print("solution: ", solution("input.txt"))
