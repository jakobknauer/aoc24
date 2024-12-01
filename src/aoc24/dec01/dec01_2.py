import sys
from collections import Counter


def main():
    a = []
    b = Counter()

    with open(sys.argv[1]) as fp:
        for line in fp:
            part1, part2 = line.split()
            a.append(int(part1))
            b[int(part2)] += 1

    result = sum(x * b[x] for x in a)

    print(result)


if __name__ == "__main__":
    main()
