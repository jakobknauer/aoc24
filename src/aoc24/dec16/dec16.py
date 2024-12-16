import sys


DIRECTIONS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}

State = tuple[int, int, int]  # x, y, direction


def main() -> None:
    with open(sys.argv[1]) as fp:
        lines = list(map(str.strip, fp.readlines()))

    walls = {(x, y) for x, line in enumerate(lines) for y, c in enumerate(line) if c == "#"}
    start = next((x, y) for x, line in enumerate(lines) for y, c in enumerate(line) if c == "S")
    end = next((x, y) for x, line in enumerate(lines) for y, c in enumerate(line) if c == "E")
    height = len(lines)
    width = len(lines[0])

    distances = {(start[0], start[1], 0): 0}
    predecessors: dict[State, set[State]] = {(start[0], start[1], 0): set()}
    visited = set()

    while not any((x, y) == end for (x, y, z) in distances):
        x, y, d = min(distances, key=lambda t: distances[t])
        dist = distances[(x, y, d)]
        del distances[(x, y, d)]
        visited.add((x, y, d))

        dx, dy = DIRECTIONS[d]
        for (nx, ny, ndir), delta in (
            ((x, y, (d + 1) % 4), 1000),
            ((x, y, (d - 1) % 4), 1000),
            ((x + dx, y + dy, d), 1),
        ):
            if (nx, ny) in walls:
                continue
            if not (0 <= nx < height and 0 <= ny < width):
                continue
            if (nx, ny, ndir) in visited:
                continue
            if (nx, ny, ndir) not in distances:
                distances[(nx, ny, ndir)] = dist + delta
                predecessors[(nx, ny, ndir)] = {(x, y, d)}
            else:
                old_distance = distances[(nx, ny, ndir)]
                if old_distance == dist + delta:
                    predecessors[(nx, ny, ndir)].add((x, y, d))
                elif dist + delta < old_distance:
                    distances[(nx, ny, ndir)] = dist + delta
                    predecessors[(nx, ny, ndir)] = {(x, y, d)}

    part1 = min(dist for (x, y, d), dist in distances.items() if (x, y) == end)

    optimal_states: set[State] = set()
    frontier = {(x, y, d) for (x, y, d), dist in distances.items() if (x, y) == end and dist == part1}
    while not frontier <= optimal_states:
        optimal_states |= frontier
        frontier = {p for (x, y, d) in frontier for p in predecessors[(x, y, d)]}

    part2 = len({(x, y) for (x, y, _) in optimal_states})
    print(part1, part2)


if __name__ == "__main__":
    main()
