import sys
from typing import Iterable, Callable
from functools import cache


def main() -> None:
    with open(sys.argv[1]) as fp:
        connections: set[tuple[str, str]] = {tuple(line.strip().split("-")) for line in fp}  # type:ignore

    computers = {c for connection in connections for c in connection}

    @cache
    def neighbors(computer: str) -> set[str]:
        n = set()
        for c1, c2 in connections:
            if c1 == computer:
                n.add(c2)
            elif c2 == computer:
                n.add(c1)
        return n

    three_cliques = set()
    for c1, c2 in connections:
        n = neighbors(c1) & neighbors(c2)
        for c3 in n:
            three_cliques.add(tuple(sorted((c1, c2, c3))))
    part1 = sum(any(c.startswith("t") for c in clique) for clique in three_cliques)

    biggest_clique: set[str] = set()
    for clique in maximal_cliques(set(), computers, set(), neighbors):
        if len(clique) > len(biggest_clique):
            biggest_clique = clique

    part2 = ",".join(sorted(biggest_clique))
    print(part1, part2)


def maximal_cliques(
    required: set[str], possible: set[str], excluded: set[str], neighbors: Callable[[str], set[str]]
) -> Iterable[set[str]]:
    """Implement the Bron-Kerbosch algorithm"""

    if not possible and not excluded:
        yield required

    for computer in list(possible):
        n = neighbors(computer)
        yield from maximal_cliques(
            required | {computer},
            possible & n,
            excluded & n,
            neighbors,
        )
        possible.remove(computer)
        excluded.add(computer)


if __name__ == "__main__":
    main()
