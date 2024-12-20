import sys
from typing import Iterable
from collections import deque

Coord = tuple[int, int]


def main() -> None:
    with open(sys.argv[1]) as fp:
        track = [line.strip() for line in fp]

    height = len(track)
    width = len(track[0])
    start = next((x, y) for x, line in enumerate(track) for y, c in enumerate(line) if c == "S")
    end = next((x, y) for x, line in enumerate(track) for y, c in enumerate(line) if c == "E")

    distances_to_start = compute_distances(track, start)
    distances_to_end = compute_distances(track, end)

    fastest = distances_to_start[end]
    part1 = 0
    part2 = 0

    for x in range(height):
        for y in range(width):
            for (rx, ry), dist in cheats_from(track, (x, y), 20):
                dist_after_cheat = distances_to_start[(x, y)] + distances_to_end[(rx, ry)] + dist
                saved = fastest - dist_after_cheat
                if saved >= 100:
                    part1 += dist <= 2
                    part2 += 1

    print(part1, part2)


def compute_distances(track: list[str], start: Coord) -> dict[Coord, int]:
    height = len(track)
    width = len(track[0])

    distances: dict[Coord, int] = {start: 0}

    to_visit: deque[Coord] = deque()
    to_visit.append(start)

    while to_visit:
        x, y = to_visit.popleft()
        d = distances[(x, y)]

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < height and 0 <= ny < width and track[nx][ny] != "#" and (nx, ny) not in distances:
                distances[(nx, ny)] = d + 1
                to_visit.append((nx, ny))

    return distances


def cheats_from(track: list[str], start: Coord, max_dist: int) -> Iterable[tuple[Coord, int]]:
    x, y = start

    if track[x][y] == "#":
        return

    height = len(track)
    width = len(track[0])

    for nx in range(max(0, x - max_dist), min(x + max_dist + 1, height)):
        dist_left = max_dist - abs(nx - x)
        for ny in range(max(0, y - dist_left), min(y + dist_left + 1, width)):
            if track[nx][ny] != "#":
                yield (nx, ny), abs(nx - x) + abs(ny - y)


if __name__ == "__main__":
    main()
