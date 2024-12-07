import sys
from itertools import islice
from math import ceil, log10


Equation = tuple[int, list[int]]


def main() -> None:
    equations: list[Equation] = []

    with open(sys.argv[1]) as fp:
        for line in fp:
            head, tail = line.split(":")
            equations.append((int(head), list(map(int, tail.split()))))

    part1 = sum(equation[0] for equation in equations if is_solvable(equation))
    part2 = sum(equation[0] for equation in equations if is_solvable2(equation))

    print(part1)
    print(part2)


def is_solvable(eq: Equation) -> bool:
    target, nums = eq

    reachable = {nums[0]}
    for n in islice(nums, 1, None):
        reachable = {x + n for x in reachable} | {x * n for x in reachable}

    return target in reachable


def is_solvable2(eq: Equation) -> bool:
    target, nums = eq

    reachable = {nums[0]}

    for n in islice(nums, 1, None):
        n_digits = ceil(log10(n))
        factor = 10**n_digits
        reachable = {x + n for x in reachable} | {x * n for x in reachable} | {x * factor + n for x in reachable}

    return target in reachable


if __name__ == "__main__":
    main()
