import sys


def main() -> None:
    with open(sys.argv[1]) as fp:
        stones = list(map(int, fp.readline().split()))

    part1 = sum(count_stones(stone, 25) for stone in stones)
    part2 = sum(count_stones(stone, 75) for stone in stones)
    print(part1, part2)


CACHE: dict[tuple[int, int], int] = {}


def count_stones(stone: int, iterations: int) -> int:
    if (stone, iterations) in CACHE:
        return CACHE[(stone, iterations)]

    if iterations == 0:
        return 1

    if stone == 0:
        result = count_stones(1, iterations - 1)
    elif len(s := str(stone)) % 2 == 0:
        part1 = int(s[len(s) // 2 :])
        part2 = int(s[: len(s) // 2])
        result = count_stones(part1, iterations - 1) + count_stones(part2, iterations - 1)
    else:
        result = count_stones(stone * 2024, iterations - 1)

    CACHE[(stone, iterations)] = result
    return result


if __name__ == "__main__":
    main()
