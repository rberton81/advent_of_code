from utils.utils import read_input

def check_report_is_increasing(report_numbers):
    if report_numbers[0] < report_numbers[1]:
        return True
    return False

def get_safe_report(input):
    safe_reports = 0
    for line in read_input(input):
        is_safe = True
        report_numbers = [int(number) for number in line.split()]
        is_increasing = check_report_is_increasing(report_numbers)

        print(f"Looking at report {report_numbers}, is_increasing: {is_increasing}")
        current_number = report_numbers[0]
        for number in report_numbers[1:]:
            diff = abs(number-current_number)
            if diff < 1 or diff > 3:
                print(f"Report not safe cause of diff")
                is_safe = False
                break
            if is_increasing and number < current_number:
                print(f"Report not safe it's increasing but not")
                is_safe = False
                break
            if not is_increasing and number > current_number:
                print(f"Report not safe it's decreasing but not")
                is_safe = False
                break

            current_number = number

        if is_safe:
            print('Report is safe')
            safe_reports += 1

    return safe_reports


assert get_safe_report("example.txt") == 2
print("solution: ", get_safe_report("input.txt"))


