import sys
from itertools import pairwise
from typing import Iterable


def main() -> None:
    result: int = 0

    with open(sys.argv[1]) as fp:
        for line in fp:
            report = list(map(int, line.split()))
            if check_report(report):
                result += 1

    print(result)


def check_report(report: list[int]) -> bool:
    return check_ascending_damper(report) or check_ascending_damper(list(reversed(report)))


def check_ascending_damper(report: list[int]) -> bool:
    return any(check_ascending((v for (j, v) in enumerate(report) if i != j)) for i in range(len(report) + 1))


def check_ascending(report: Iterable[int]) -> bool:
    return all((1 <= (y - x) <= 3) for (x, y) in pairwise(report))


if __name__ == "__main__":
    main()
