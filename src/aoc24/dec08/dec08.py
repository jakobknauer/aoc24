import sys

Coord = tuple[int, int]


def part1() -> None:
    antennas: dict[str, list[Coord]] = {}
    height: int = 0
    width: int = 0

    with open(sys.argv[1]) as fp:
        for x, line in enumerate(fp):
            height = max(x + 1, height)
            for y, c in enumerate(line.strip()):
                width = max(y + 1, width)
                if c != ".":
                    if c not in antennas:
                        antennas[c] = []
                    antennas[c].append((x, y))

    antinodes: set[Coord] = set()

    for _, a in antennas.items():
        for i1 in range(len(a)):
            for i2 in range(i1 + 1, len(a)):
                x1, y1 = a[i1]
                x2, y2 = a[i2]
                dx, dy = x1 - x2, y1 - y2

                antinodes.add((x1 + dx, y1 + dy))
                antinodes.add((x2 - dx, y2 - dy))

    filtered_antinodes = {(x, y) for (x, y) in antinodes if 0 <= x < height and 0 <= y < width}

    print(len(filtered_antinodes))


def part2() -> None:
    antennas: dict[str, list[Coord]] = {}
    height: int = 0
    width: int = 0

    with open(sys.argv[1]) as fp:
        for x, line in enumerate(fp):
            height = max(x + 1, height)
            for y, c in enumerate(line.strip()):
                width = max(y + 1, width)
                if c != ".":
                    if c not in antennas:
                        antennas[c] = []
                    antennas[c].append((x, y))

    antinodes: set[Coord] = set()

    for _, a in antennas.items():
        for i1 in range(len(a)):
            for i2 in range(i1 + 1, len(a)):
                x1, y1 = a[i1]
                x2, y2 = a[i2]
                dx, dy = x1 - x2, y1 - y2

                for i in range(-max(width, height) - 1, max(width, height) + 1):
                    antinodes.add((x1 + i * dx, y1 + i * dy))

    filtered_antinodes = {(x, y) for (x, y) in antinodes if 0 <= x < height and 0 <= y < width}

    print(len(filtered_antinodes))


if __name__ == "__main__":
    part2()
