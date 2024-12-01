import sys


def main():
    a = []
    b = []

    with open(sys.argv[1]) as fp:
        for line in fp:
            part1, part2 = line.split()
            a.append(int(part1))
            b.append(int(part2))

    a.sort()
    b.sort()

    result = sum(abs(x - y) for (x, y) in zip(a, b))

    print(result)


if __name__ == "__main__":
    main()
