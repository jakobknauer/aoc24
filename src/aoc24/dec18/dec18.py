import sys

Coord = tuple[int, int]


def main() -> None:
    with open(sys.argv[1]) as fp:
        coordinates = [tuple(map(int, line.split(","))) for line in fp]

    width = 71
    height = 71
    target = (height - 1, width - 1)

    for i in range(1024, len(coordinates)):
        corrupted = set(coordinates[:i])

        visited: set[Coord] = set()
        frontier = {(0, 0)}
        distance = 0

        while target not in frontier:
            visited |= frontier
            frontier = {
                (xx, yy)
                for (x, y) in frontier
                for (xx, yy) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                if 0 <= xx < width and 0 <= yy < height and (xx, yy) not in corrupted and (xx, yy) not in visited
            }
            if not frontier:
                break
            distance += 1

        if target not in frontier:
            print(coordinates[i - 1])
            break


if __name__ == "__main__":
    main()
