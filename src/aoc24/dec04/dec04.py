import sys


def part1():
    with open(sys.argv[1]) as fp:
        puzzle = fp.readlines()

    directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

    print(len(puzzle))
    print(len(puzzle[0]))

    result = 0
    for x in range(len(puzzle)):
        for y in range(len(puzzle[0])):
            for d in directions:
                if find_xmas(puzzle, x, y, d):
                    result += 1

    print(result)


def find_xmas(puzzle, x, y, direction) -> bool:
    dx, dy = direction

    max_x = x + 3 * dx
    max_y = y + 3 * dy

    if not (0 <= max_x < len(puzzle) and 0 <= max_y < len(puzzle[0])):
        return False

    # print("".join(puzzle[x + i * dx][y + i * dy] for i in range(4)))
    return "".join(puzzle[x + i * dx][y + i * dy] for i in range(4)) == "XMAS"


def part2():
    with open(sys.argv[1]) as fp:
        puzzle = fp.readlines()

    result = 0

    for x in range(1, len(puzzle) - 1):
        for y in range(1, len(puzzle[0]) - 1):
            s1 = "".join((puzzle[x - 1][y - 1], puzzle[x][y], puzzle[x + 1][y + 1]))
            s2 = "".join((puzzle[x - 1][y + 1], puzzle[x][y], puzzle[x + 1][y - 1]))

            if (s1 == "MAS" or s1 == "SAM") and (s2 == "MAS" or s2 == "SAM"):
                result += 1

    print(result)


if __name__ == "__main__":
    part2()
