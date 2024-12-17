import sys
from functools import cache


def run(A, B, C, program) -> list[int]:
    pc = 0

    output: list[int] = []

    while pc < len(program):
        inst = program[pc]
        op = program[pc + 1]

        match inst:
            case 0:
                A = A // (2 ** combo(A, B, C, op))
                pc += 2
            case 1:
                B = B ^ op
                pc += 2
            case 2:
                B = combo(A, B, C, op) % 8
                pc += 2
            case 3 if A != 0:
                pc = op
            case 3 if A == 0:
                pc += 2
            case 4:
                B = B ^ C
                pc += 2
            case 5:
                output.append(combo(A, B, C, op) % 8)
                pc += 2
            case 6:
                B = A // (2 ** combo(A, B, C, op))
                pc += 2
            case 7:
                C = A // (2 ** combo(A, B, C, op))
                pc += 2
            case _:
                raise ValueError(f"Unexpected instruction '{inst}'.")

    return output


@cache
def run_optimized(A: int) -> list[int]:
    B = A % 8
    B = B ^ 2
    C = A // (2**B)
    B = B ^ 3
    B = B ^ C

    A = A // 8

    if A == 0:
        return [B % 8]
    else:
        return [B % 8] + run_optimized(A)


def combo(A, B, C, op) -> int:
    match op:
        case 0 | 1 | 2 | 3:
            return op
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case _:
            raise ValueError(f"Unexpected combo operand '{op}'.")


def main() -> None:
    with open(sys.argv[1]) as fp:
        A = int(fp.readline().strip())
        B = int(fp.readline().strip())
        C = int(fp.readline().strip())
        program = list(map(int, fp.readline().split(",")))

    part1 = run(A, B, C, program)
    print(part1)

    part2 = 0

    constructed = 0
    remaining = list(program)
    while constructed < len(program):
        A = 8**7
        while True:
            # result = run(A, B, C, program)  # works for all programs
            result = run_optimized(A)  # specific to the given program

            if all(x == y for (x, y) in zip(result, remaining)):
                part2 += (8**constructed) * A
                constructed += len(result)
                remaining = program[constructed:]
                break
            A += 1

    print(part2)


if __name__ == "__main__":
    main()
