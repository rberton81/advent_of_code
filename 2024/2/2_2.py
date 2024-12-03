from utils.utils import read_input

class Report:
    class UnsafeError(Exception):
        pass

    def report_is_increasing(self):
        if self.numbers[0] < self.numbers[1]:
            return True
        return False

    def __init__(self, numbers, problem_dampener_used=False):
        self.numbers = numbers
        self.is_increasing = self.report_is_increasing()
        self.problem_dampener_used = problem_dampener_used

    def __repr__(self):
        return f"Report({self.numbers})"

    def has_faults(self):
        current_number = self.numbers[0]
        is_increasing = self.is_increasing

        for index, number in enumerate(self.numbers[1:]):
            if is_increasing is None and current_number != number:
                is_increasing = current_number < number

            diff = abs(number-current_number)
            if diff < 1 or diff > 3:
                if self.problem_dampener_used:
                    raise Report.UnsafeError(f"Report is unsafe: {self.numbers}")
                if index == 0: # Removes 1st number
                    if Report(self.numbers[1:], problem_dampener_used=True).is_safe():
                        return False
                    is_increasing=None # Removes 2nd number
                self.problem_dampener_used = True
                continue
            elif (is_increasing and number < current_number) or (not is_increasing and number > current_number):
                if self.problem_dampener_used:
                    raise Report.UnsafeError(f"Report is unsafe: {self.numbers}")
                if index == 1:
                    is_increasing = None
                if index > 1 and Report([self.numbers[index-1]] + self.numbers[index+1:], problem_dampener_used=True).is_safe():
                    return False
                self.problem_dampener_used = True
                continue
            current_number = number
        return False
    
    def is_safe(self):
        try:
            return not self.has_faults()
        except Report.UnsafeError:
            return False

def get_safe_reports(input):
    safe_reports = 0
    for line in read_input(input):
        numbers = [int(number) for number in line.split()]
        report = Report(numbers)
        if report.is_safe():
            safe_reports += 1
    return safe_reports

assert get_safe_reports("example.txt") == 7
print("solution: ", get_safe_reports("input.txt"))

