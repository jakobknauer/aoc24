import sys
from functools import cache


def main():
    with open(sys.argv[1]) as fp:
        towels = [t.strip() for t in fp.readline().split(",")]
        fp.readline()
        designs = [d.strip() for d in fp]

    @cache
    def design_achievable(design: str) -> bool:
        if not design:
            return True

        return any(possibilities(design[len(towel) :]) for towel in towels if design.startswith(towel))

    @cache
    def possibilities(design: str) -> int:
        if not design:
            return 1

        return sum(possibilities(design[len(towel) :]) for towel in towels if design.startswith(towel))

    part1 = sum(map(design_achievable, designs))
    part2 = sum(map(possibilities, designs))

    print(part1, part2)


if __name__ == "__main__":
    main()
