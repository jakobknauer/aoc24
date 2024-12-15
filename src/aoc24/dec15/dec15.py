import sys
from typing import Iterable


DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}


def part1() -> None:
    warehouse = []
    directions: list[str] = []

    with open(sys.argv[1]) as fp:
        while (line := fp.readline().strip()) != "":
            warehouse.append(list(line))

        for line in fp:
            directions += line.strip()

    rx, ry = next((x, y) for (x, line) in enumerate(warehouse) for (y, c) in enumerate(line) if c == "@")

    warehouse[rx][ry] = "."

    for d in directions:
        dx, dy = DIRECTIONS[d]

        nx, ny = rx + dx, ry + dy
        tx, ty = nx, ny
        while warehouse[tx][ty] == "O":
            tx += dx
            ty += dy

        if warehouse[tx][ty] == "#":
            continue

        if (tx, ty) != (nx, ny):
            warehouse[tx][ty] = "O"

        warehouse[nx][ny] = "."
        rx, ry = nx, ny

    result = sum(100 * x + y for (x, line) in enumerate(warehouse) for (y, c) in enumerate(line) if c == "O")
    print(result)


Coord = tuple[int, int]


def part2() -> None:
    walls: set[Coord] = set()
    boxes: list[Coord] = []
    robot: Coord = (0, 0)
    directions: list[str] = []
    width: int = 0
    height: int = 0

    with open(sys.argv[1]) as fp:
        x = 0
        while (line := fp.readline().strip()) != "":
            height = max(height, x + 1)
            for y, c in enumerate(line):
                width = max(width, 2 * (y + 1))
                if c == "#":
                    walls.add((x, 2 * y))
                    walls.add((x, 2 * y + 1))
                elif c == "@":
                    robot = (x, 2 * y)
                elif c == "O":
                    boxes.append((x, 2 * y))
            x += 1

        for line in fp:
            directions += line.strip()

    for d in directions:
        rx, ry = robot
        dx, dy = DIRECTIONS[d]

        if (rx + dx, ry + dy) in walls:
            continue

        # Get box indices blocking robot
        relevant_box_indices = list(get_blocking_box_index(boxes, [robot], d))

        # Recursively get all blocking boxes
        next_box_indices = set(relevant_box_indices)
        while next_box_indices:
            current_box_positions = {boxes[i] for i in next_box_indices}
            current_box_positions |= {(x, y + 1) for (x, y) in current_box_positions}
            next_box_indices = set(get_blocking_box_index(boxes, current_box_positions, d))

            relevant_box_indices += next_box_indices

        relevant_box_positions = {boxes[i] for i in relevant_box_indices}
        relevant_box_positions |= {(x, y + 1) for (x, y) in relevant_box_positions}

        # Check if any of the boxes is blocked by a wall
        blocked = any((x + dx, y + dy) in walls for (x, y) in relevant_box_positions)

        if blocked:
            continue

        # Move boxes
        for i in relevant_box_indices:
            x, y = boxes[i]
            boxes[i] = (x + dx, y + dy)

        # Move robot
        robot = rx + dx, ry + dy

    result = sum(100 * x + y for (x, y) in boxes)
    print(result)


def get_blocking_box_index(boxes: list[Coord], pos: Iterable[Coord], d: str) -> Iterable[int]:
    for x, y in pos:
        if d == "<":
            if (x, y - 2) in boxes:
                yield boxes.index((x, y - 2))
        elif d == ">":
            if (x, y + 1) in boxes:
                yield boxes.index((x, y + 1))
        elif d == "^":
            if (x - 1, y) in boxes:
                yield boxes.index((x - 1, y))
            if (x - 1, y - 1) in boxes:
                yield boxes.index((x - 1, y - 1))
        elif d == "v":
            if (x + 1, y) in boxes:
                yield boxes.index((x + 1, y))
            if (x + 1, y - 1) in boxes:
                yield boxes.index((x + 1, y - 1))


def print_warehouse(boxes, walls, robot, width, height):
    for x in range(height):
        for y in range(width):
            if (x, y) in boxes:
                print("[", end="")
            elif (x, y - 1) in boxes:
                print("]", end="")
            elif (x, y) in walls:
                print("#", end="")
            elif (x, y) == robot:
                print("@", end="")
            else:
                print(" ", end="")
        print("")


if __name__ == "__main__":
    part2()
