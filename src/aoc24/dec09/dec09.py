import sys


BlockSpec = tuple[int, int]  # start_index, size
FreeBlock = BlockSpec
FileId = int
FilledBlock = tuple[BlockSpec, FileId]


def main() -> None:
    with open(sys.argv[1], "r") as fp:
        diskmap = list(map(int, fp.readline().strip()))

    free_blocks, filled_blocks = decompress(diskmap)
    # compact(disk)
    compacted_disk = compact2(free_blocks, filled_blocks)
    checksum = compute_checksum2(compacted_disk)
    print(checksum)


def decompress(diskmap: list[int]) -> tuple[list[FreeBlock], list[FilledBlock]]:
    free_blocks: list[FreeBlock] = []
    filled_blocks: list[FilledBlock] = []

    free_block: bool = False
    fileno: int = 0
    current_pos = 0

    for block_size in diskmap:
        if free_block:
            free_blocks.append((current_pos, block_size))
        else:
            filled_blocks.append(((current_pos, block_size), fileno))
            fileno += 1
        free_block = not free_block
        current_pos += block_size

    return free_blocks, filled_blocks


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


def compact2(free_blocks: list[FreeBlock], filled_blocks: list[FilledBlock]) -> list[FilledBlock]:
    compacted_disk: list[FilledBlock] = []

    for (file_pos, file_size), file_id in reversed(filled_blocks):
        found_free_block = False
        for free_block_index, (free_pos, free_size) in enumerate(free_blocks):
            if free_pos >= file_pos:
                break
            if free_size >= file_size:
                found_free_block = True
                break

        if not found_free_block:
            compacted_disk.append(((file_pos, file_size), file_id))
        elif free_size == file_size:
            compacted_disk.append(((free_pos, file_size), file_id))
            del free_blocks[free_block_index]
        else:
            compacted_disk.append(((free_pos, file_size), file_id))
            del free_blocks[free_block_index]
            free_blocks.insert(free_block_index, (free_pos + file_size, free_size - file_size))

    return compacted_disk


# def compute_checksum(disk: list[int | None]) -> int:
#     return sum(i * n for (i, n) in enumerate(disk) if n is not None)


def compute_checksum2(disk: list[FilledBlock]) -> int:
    checksum = 0

    for (pos, size), file_id in disk:
        for i in range(pos, pos + size):
            checksum += i * file_id

    return checksum


if __name__ == "__main__":
    main()
