import sys
from itertools import pairwise


def main() -> None:
    result: int = 0

    with open(sys.argv[1]) as fp:
        for line in fp:
            report = list(map(int, line.split()))
            if check_report(report):
                result += 1

    print(result)


def check_report(report: list[int]) -> bool:
    if len(report) <= 1:
        return True

    if report[0] < report[1]:
        return check_ascending(report)
    elif report[0] > report[1]:
        return check_descending(report)
    else:
        return False


def check_ascending(report: list[int]) -> bool:
    return all((1 <= (y - x) <= 3) for (x, y) in pairwise(report))


def check_descending(report: list[int]) -> bool:
    return all((1 <= (x - y) <= 3) for (x, y) in pairwise(report))


if __name__ == "__main__":
    main()
