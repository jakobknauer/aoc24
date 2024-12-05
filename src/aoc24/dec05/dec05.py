import sys
from functools import cmp_to_key


def part1() -> None:
    rules = []
    reports = []

    with open(sys.argv[1]) as fp:
        while (line := fp.readline()) != "\n":
            rules.append(tuple(map(int, line.split("|"))))

        for line in fp:
            r = list(map(int, line.split(",")))
            pivot = r[len(r) // 2]
            report = dict((v, i) for (i, v) in enumerate(r))
            reports.append((pivot, report))

    result = 0

    for pivot, report in reports:
        failed = False
        for a, b in rules:
            if (a in report) and (b in report) and (report[a] > report[b]):
                failed = True
                break

        if not failed:
            result += pivot

    print(result)


def part2() -> None:
    rules: set[tuple[int, int]] = set()

    reports = []

    with open(sys.argv[1]) as fp:
        while (line := fp.readline()) != "\n":
            a, b = map(int, line.split("|"))
            rules.add((a, b))

        for line in fp:
            r = list(map(int, line.split(",")))
            pivot = r[len(r) // 2]
            report = dict((v, i) for (i, v) in enumerate(r))
            reports.append((pivot, report))

    result = 0
    for pivot, report in reports:
        if check(report, rules) is None:
            continue

        while (broken_rule := check(report, rules)) is not None:
            a, b = broken_rule
            report[a], report[b] = report[b], report[a]

        report_items = list(report.keys())
        report_items.sort(key=lambda v: report[v])

        result += report_items[len(report_items) // 2]

    print(result)


def check(report, rules: set[tuple[int, int]]):
    for a, b in rules:
        if (a in report) and (b in report) and (report[a] > report[b]):
            return (a, b)
    return None


if __name__ == "__main__":
    part2()
