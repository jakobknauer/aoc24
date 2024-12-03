import re
import sys


def part1() -> None:
    with open(sys.argv[1], "r") as fp:
        text = fp.read()

    pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
    result = sum(int(a) * int(b) for a, b in pattern.findall(text))
    print(result)


def part2() -> None:
    with open(sys.argv[1], "r") as fp:
        text = fp.read()

    do = re.compile(r"do\(\)")
    dont = re.compile(r"don't\(\)")
    pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

    result = 0

    while text:
        # find first don't() marker
        dont_marker: re.Match | None = dont.search(text)

        if dont_marker:
            enabled = text[: dont_marker.start()]
            result += sum(int(a) * int(b) for a, b in pattern.findall(enabled))
            text = text[dont_marker.end() :]
            do_marker: re.Match | None = do.search(text)
            if do_marker:
                text = text[do_marker.end() :]
            else:
                break

        else:
            result += sum(int(a) * int(b) for a, b in pattern.findall(text))
            break

    print(result)


if __name__ == "__main__":
    part2()
