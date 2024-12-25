import sys
from itertools import islice


def main() -> None:
    keys = []
    locks = []
    with open(sys.argv[1]) as fp:
        while (first := fp.readline()) != "":
            lines = map(lambda l: l.strip(), islice(fp, 5))
            thing = [col.count("#") for col in zip(*lines)]

            if first.startswith("#"):
                locks.append(thing)
            else:
                keys.append(thing)

            fp.readline()
            fp.readline()

    part1 = sum(all(l + k <= 5 for (l, k) in zip(lock, key)) for lock in locks for key in keys)
    print(part1)


if __name__ == "__main__":
    main()
