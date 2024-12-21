import sys
from collections import deque
from functools import cache
from itertools import product, pairwise
from typing import Iterable

Coord = tuple[int, int]
Path = list[str]


NUMERIC_KEYPAD: dict[str, Coord] = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

DIRECTIONAL_KEYPAD: dict[str, Coord] = {
    "^": (0, 1),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "A": (0, 2),
}

DIRECTIONS: dict[str, Coord] = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


def shortest_paths_numeric_keypad(start: Coord, end: Coord) -> list[Path]:
    paths: dict[Coord, list[Path]] = {start: [[]]}

    to_visit: deque[Coord] = deque([start])
    visited: set[Coord] = set()

    while to_visit:
        current = to_visit.popleft()

        if current == end:
            return paths[end]

        for direction_name, direction in DIRECTIONS.items():
            new_coord = (current[0] + direction[0], current[1] + direction[1])
            if new_coord not in NUMERIC_KEYPAD.values() or new_coord in visited:
                continue

            if new_coord not in paths:
                paths[new_coord] = []
                to_visit.append(new_coord)

            paths[new_coord] += (p + [direction_name] for p in paths[current])

        visited.add(current)

    return []


@cache
def shortest_paths_directional_keypad(start: Coord, end: Coord) -> list[Path]:
    paths: dict[Coord, list[Path]] = {start: [[]]}

    to_visit: deque[Coord] = deque([start])
    visited: set[Coord] = set()

    while to_visit:
        current = to_visit.popleft()

        if current == end:
            return paths[end]

        for direction_name, direction in DIRECTIONS.items():
            new_coord = (current[0] + direction[0], current[1] + direction[1])
            if new_coord not in DIRECTIONAL_KEYPAD.values() or new_coord in visited:
                continue

            if new_coord not in paths:
                paths[new_coord] = []
                to_visit.append(new_coord)

            paths[new_coord] += (p + [direction_name] for p in paths[current])

        visited.add(current)

    return []


def main() -> None:
    with open(sys.argv[1], "r") as fp:
        codes = [line.strip() for line in fp]

    # Change to 3 for part 1
    n_robots = 26
    # directional[i][start,end] should contain the number of presses on the human keyboard to go from start to end on the ith keyboard, and press end
    directional: list[dict[tuple[Coord, Coord], int]] = []
    # numerical[start,end] should contain the number of presses on the human keyboard to make the last robot go from start to end, and press end
    numerical: dict[tuple[Coord, Coord], int] = {}

    # dp[0] refers to the human keyboard, so there is no cost for going from start to end, just for pressing end
    directional.append({(start, end): 1 for (start, end) in product(DIRECTIONAL_KEYPAD.values(), repeat=2)})

    for i in range(1, n_robots):
        directional.append({})
        for start, end in product(DIRECTIONAL_KEYPAD.values(), repeat=2):
            paths = shortest_paths_directional_keypad(start, end)
            min_cost = min(
                sum(
                    directional[i - 1][DIRECTIONAL_KEYPAD[d1], DIRECTIONAL_KEYPAD[d2]]
                    for (d1, d2) in pairwise(["A"] + path + ["A"])
                )
                for path in paths
            )
            directional[i][start, end] = min_cost

    for start, end in product(NUMERIC_KEYPAD.values(), repeat=2):
        for end in NUMERIC_KEYPAD.values():
            paths = shortest_paths_numeric_keypad(start, end)

            min_cost = min(
                sum(
                    directional[-1][DIRECTIONAL_KEYPAD[d1], DIRECTIONAL_KEYPAD[d2]]
                    for (d1, d2) in pairwise(["A"] + path + ["A"])
                )
                for path in paths
            )
            numerical[start, end] = min_cost

    result = 0
    for code in codes:
        cost = sum(numerical[NUMERIC_KEYPAD[n1], NUMERIC_KEYPAD[n2]] for n1, n2 in pairwise("A" + code))
        result += cost * int(code[:-1])

    print(result)


if __name__ == "__main__":
    main()
