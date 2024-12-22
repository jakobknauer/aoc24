import sys
from itertools import pairwise
from collections import Counter


type Sequence = tuple[int, int, int, int]


def main() -> None:
    with open(sys.argv[1]) as fp:
        initial_secrets = list(map(int, fp))

    part1 = 0
    all_sequences: Counter[Sequence] = Counter()

    for initial_secret in initial_secrets:
        chain = secret_chain(initial_secret, 2000)
        part1 += chain[-1]
        all_sequences.update(sequences_for(chain))

    part2 = max(all_sequences.values())

    print(part1, part2)


def secret_chain(secret: int, rounds: int) -> list[int]:
    secrets = []

    for _ in range(rounds):
        secret ^= secret << 6
        secret %= 16777216

        secret ^= secret >> 5
        secret %= 16777216

        secret ^= secret << 11
        secret %= 16777216

        secrets.append(secret)

    return secrets


def sequences_for(secrets: list[int]) -> dict[Sequence, int]:
    sequences: dict[Sequence, int] = {}

    reduced = (s % 10 for s in secrets)
    changes = [b - a for a, b in pairwise(reduced)]

    for i in range(0, len(changes) - 3):
        seq = (changes[i], changes[i + 1], changes[i + 2], changes[i + 3])

        if seq not in sequences:
            sequences[seq] = secrets[i + 3] % 10  # type: ignore

    return sequences


if __name__ == "__main__":
    main()
