import sys
import re


pattern = re.compile("p=([-]?[0-9]+),([-]?[0-9]+) v=([-]?[0-9]+),([-]?[0-9]+)")


def main() -> None:
    robots = []
    with open(sys.argv[1]) as fp:
        for line in fp:
            match = pattern.match(line)
            assert match
            x, y, vx, vy = map(int, match.group(1, 2, 3, 4))
            robots.append(((x, y), (vx, vy)))

    width = 101
    height = 103
    steps = 100

    q = [0, 0, 0, 0]
    end_positions = (((x + steps * vx) % width, (y + steps * vy) % height) for ((x, y), (vx, vy)) in robots)
    for x, y in end_positions:
        if x < width // 2:
            if y < height // 2:
                q[0] += 1
            elif y > height // 2:
                q[1] += 1
        elif x > width // 2:
            if y < height // 2:
                q[2] += 1
            elif y > height // 2:
                q[3] += 1

    part1 = q[0] * q[1] * q[2] * q[3]
    print(part1)

    steps = 7093
    positions = {((x + steps * vx) % width, (y + steps * vy) % height) for ((x, y), (vx, vy)) in robots}
    for y in range(height):
        for x in range(width):
            if (x, y) in positions:
                print("X", end="")
            else:
                print(" ", end="")
        print("")


if __name__ == "__main__":
    main()
