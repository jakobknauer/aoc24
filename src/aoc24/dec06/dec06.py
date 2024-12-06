import sys

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

Coord = tuple[int, int]


def does_loop(
    obstacles: set[tuple[int, int]], p0: tuple[int, int], width: int, height: int, direction: int
) -> tuple[set[tuple[int, int, int]], bool]:
    visited_states: set[tuple[int, int, int]] = set()
    px, py = p0
    while 0 <= px < height and 0 <= py < width:
        dx, dy = DIRECTIONS[direction]
        nx, ny = px + dx, py + dy
        if (nx, ny) in obstacles:
            direction = (direction + 1) % 4
        else:
            px, py = nx, ny
            if (px, py, direction) in visited_states:
                return visited_states, True
            else:
                visited_states.add((px, py, direction))
    return visited_states, False


def main() -> None:
    obstacles: set[tuple[int, int]] = set()
    p0: tuple[int, int]
    height, width = 0, 0

    with open(sys.argv[1]) as fp:
        for x, line in enumerate(fp):
            height = max(height, x + 1)
            for y, c in enumerate(line):
                width = max(width, y + 1)
                if c == "#":
                    obstacles.add((x, y))
                elif c == "^":
                    p0 = x, y

    visited_states, _ = does_loop(obstacles, p0, width, height, 0)
    visited_coordinates = set((x, y) for (x, y, _) in visited_states)

    print(len(visited_coordinates))  # Part 1

    n_options = 0
    for x, y in visited_coordinates:
        if (x, y) in obstacles or (x, y) == p0:
            continue

        obstacles.add((x, y))
        _, loop = does_loop(obstacles, p0, width, height, 0)
        if loop:
            n_options += 1
        obstacles.remove((x, y))

    print(n_options)  # Part 2


if __name__ == "__main__":
    main()
