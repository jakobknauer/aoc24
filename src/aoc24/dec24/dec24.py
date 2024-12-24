import sys
from itertools import takewhile
from functools import cache
import re


def main() -> None:
    with open(sys.argv[1]) as fp:
        initial_values = {
            s[0][:3]: (s[1] == "1") for s in (line.strip().split(" ") for line in takewhile(lambda l: l != "\n", fp))
        }

        pattern = r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)"
        gates = {
            m[3]: (m[1], m[0], m[2]) for m in (re.match(pattern, line.strip()).groups() for line in fp)  # type:ignore
        }

    part1 = simulate(initial_values, gates)
    print(part1)

    pairs = (
        ("z05", "bpf"),
        ("z11", "hcc"),
        ("hqc", "qcw"),
        ("fdw", "z35"),
    )
    for g1, g2 in pairs:
        gates[g1], gates[g2] = gates[g2], gates[g1]

    for i in range(45):
        for k in initial_values:
            initial_values[k] = False
        initial_values[f"x{i:02d}"] = True
        initial_values[f"y{i:02d}"] = True
        result = simulate(initial_values, gates)

        if result != 2 ** (i + 1):
            print(f"Error at bit {i}")

    part2 = ",".join(sorted(g for pair in pairs for g in pair))
    print(part2)


def simulate(initial_values, gates):
    @cache
    def get_output(gate: str) -> bool:
        if gate in initial_values:
            return initial_values[gate]

        op, a, b = gates[gate]
        match op:
            case "AND":
                return get_output(a) and get_output(b)
            case "OR":
                return get_output(a) or get_output(b)
            case "XOR":
                return get_output(a) != get_output(b)
            case _:
                raise ValueError(f"Unknown gate type: {op}")

    all_gates = set(gates.keys()) | set(initial_values.keys())
    z_gates = sorted((g for g in all_gates if g.startswith("z")), reverse=True)

    output = 0
    for g in z_gates:
        output = (output << 1) | get_output(g)
    return output


if __name__ == "__main__":
    main()
