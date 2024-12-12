import sys
from typing import Iterable, Callable

Coord = tuple[int, int]
Fence = tuple[int, int, tuple[int, int]]  # x, y, direction

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def main() -> None:
    with open(sys.argv[1]) as fp:
        garden = [list(line.strip()) for line in fp]

    height = len(garden)
    width = len(garden[0])

    def neighbors(p: Coord) -> Iterable[Coord]:
        x, y = p
        return (
            (xx, yy)
            for (xx, yy) in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1))
            if 0 <= xx < height and 0 <= yy < width and garden[x][y] == garden[xx][yy]
        )

    all_plots = ((x, y) for x in range(height) for y in range(width))
    costs = map(cost, iterate_regions(all_plots, neighbors))
    part1, part2 = map(sum, zip(*costs))
    print(part1, part2)


def cost(plot: set[tuple[int, int]]) -> tuple[int, int]:
    area = len(plot)
    segments = {
        (nx, ny, (dx, dy)) for (x, y) in plot for (dx, dy) in DIRECTIONS if (nx := x + dx, ny := y + dy) not in plot
    }

    def neighbors(segment: Fence) -> Iterable[Fence]:
        x, y, d = segment
        candidates = (
            ((x, y + 1, d), (x, y - 1, d)) if d in {DIRECTIONS[0], DIRECTIONS[1]} else ((x + 1, y, d), (x - 1, y, d))
        )
        return (c for c in candidates if c in segments)

    fences = sum(1 for _ in iterate_regions(segments, neighbors))

    return area * len(segments), area * fences


def iterate_regions[T](points: Iterable[T], neighbors: Callable[[T], Iterable[T]]) -> Iterable[set[T]]:
    visited = set()

    for p in points:
        if p in visited:
            continue

        region: set[T] = set()
        frontier = {p}
        while not frontier <= region:
            region |= frontier
            frontier = {n for f in frontier for n in neighbors(f) if n not in region}

        visited |= region
        yield region


if __name__ == "__main__":
    main()
