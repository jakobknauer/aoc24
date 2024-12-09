import sys


def main() -> None:
    with open(sys.argv[1], "r") as fp:
        diskmap = list(map(int, fp.readline().strip()))

    disk = decompress(diskmap)
    # compact(disk)
    compact2(disk)
    checksum = compute_checksum2(disk)
    print(checksum)


def decompress(diskmap: list[int]) -> list[tuple[int, int | None]]:
    result: list[tuple[int, int | None]] = []
    empty: bool = False
    fileno: int = 0

    for n in diskmap:
        if empty:
            result.append((n, None))
        else:
            result.append((n, fileno))
            fileno += 1
        empty = not empty

    return result


# def compact(disk: list[int, int | None]) -> None:
#     empty_slot: int = 0
#     filled_slot: int = len(disk) - 1
#
#     while disk[empty_slot] is not None:
#         empty_slot += 1
#
#     while disk[filled_slot] is None:
#         filled_slot -= 1
#
#     while empty_slot < filled_slot:
#         disk[empty_slot], disk[filled_slot] = disk[filled_slot], disk[empty_slot]
#         while disk[empty_slot] is not None:
#             empty_slot += 1
#
#         while disk[filled_slot] is None:
#             filled_slot -= 1


def compact2(disk: list[tuple[int, int | None]]) -> None:
    highest_id = max(id_ for (_, id_) in disk if id_ is not None)

    for file_id in range(highest_id, -1, -1):
        file_index, file_size = next((index, size) for (index, (size, id_)) in enumerate(disk) if id_ == file_id)

        free_index = 0
        while free_index < file_index:

            (size, id_) = disk[free_index]
            if id_ is None and size >= file_size:
                break

            free_index += 1

        if free_index == file_index:
            continue

        free_size, _ = disk[free_index]

        if free_size == file_size:
            disk[free_index] = (free_size, file_id)
            disk[file_index] = (file_size, None)
        else:
            disk[file_index] = (file_size, None)
            disk[free_index] = (file_size, file_id)
            disk.insert(free_index + 1, (free_size - file_size, None))


# def compute_checksum(disk: list[int | None]) -> int:
#     return sum(i * n for (i, n) in enumerate(disk) if n is not None)


def compute_checksum2(disk: list[tuple[int, int | None]]) -> int:
    checksum = 0
    current_pos = 0
    for size, id_ in disk:
        if id_ is not None:
            for i in range(current_pos, current_pos + size):
                checksum += id_ * i
        current_pos += size

    return checksum


if __name__ == "__main__":
    main()
