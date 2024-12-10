import sys


def main():
    with open(sys.argv[1]) as fp:
        topology = [list(map(int, line.strip())) for line in fp]

    part1 = sum(
        count_reachable_summits(topology, x, y, set)
        for x in range(len(topology))
        for y in range(len(topology[0]))
        if topology[x][y] == 0
    )
    print(part1)

    part2 = sum(
        count_reachable_summits(topology, x, y, list)
        for x in range(len(topology))
        for y in range(len(topology[0]))
        if topology[x][y] == 0
    )
    print(part2)


def count_reachable_summits(topology, x0, y0, container) -> int:
    current_nodes = container(((x0, y0),))

    for level in range(1, 10):
        current_nodes = container(n for (x, y) in current_nodes for n in neighbors(topology, x, y, level))

    return len(current_nodes)


def neighbors(topology, x0, y0, level):
    return (
        (x, y)
        for (x, y) in ((x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1))
        if 0 <= x < len(topology) and 0 <= y < len(topology[0]) and topology[x][y] == level
    )


if __name__ == "__main__":
    main()
