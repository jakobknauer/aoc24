import sys
from itertools import batched
from fractions import Fraction


ERROR = 10000000000000


def main() -> None:
    machines1 = []
    machines2 = []

    with open(sys.argv[1]) as fp:
        all_lines = fp.readlines()

        for batch in batched(all_lines, n=4):
            a, b, target, _ = batch

            A = tuple(map(int, a.split()))
            B = tuple(map(int, b.split()))
            T = tuple(map(int, target.split()))

            machines1.append((A, B, T))
            machines2.append((A, B, (T[0] + ERROR, T[1] + ERROR)))

    part1 = sum(map(cost, machines1))
    part2 = sum(map(cost, machines2))

    print(part1)
    print(part2)


def cost(machine) -> int:
    """
    Solve P * (A | B) = T for P,
    where P = (pa pb), T = (tx ty), A = (ax ay), B = (bx by)
    """
    A, B, T = machine

    ax, ay = A
    bx, by = B
    tx, ty = T

    detinv = Fraction(1, ax * by - bx * ay)

    pa = detinv * (tx * by - ty * bx)
    pb = detinv * (-tx * ay + ty * ax)

    return (3 * pa + pb) if pa.is_integer() and pb.is_integer() else 0


if __name__ == "__main__":
    main()
