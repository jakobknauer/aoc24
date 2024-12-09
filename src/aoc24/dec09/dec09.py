import sys


BlockSpec = tuple[int, int]  # start_index, size
FreeBlock = BlockSpec
FileId = int
FilledBlock = tuple[BlockSpec, FileId]


def main() -> None:
    with open(sys.argv[1], "r") as fp:
        diskmap = list(map(int, fp.readline().strip()))

    # free_blocks, filled_blocks = decompress_blocks(diskmap)  # Part 1
    free_blocks, filled_blocks = decompress_files(diskmap)  # Part2
    compact(free_blocks, filled_blocks)
    checksum = compute_checksum(filled_blocks)
    print(checksum)


def decompress_blocks(diskmap: list[int]) -> tuple[list[FreeBlock], list[FilledBlock]]:
    free_blocks: list[FreeBlock] = []
    filled_blocks: list[FilledBlock] = []

    free_block: bool = False
    fileno: int = 0
    current_pos = 0

    for block_size in diskmap:
        if free_block:
            for i in range(block_size):
                free_blocks.append((current_pos + i, 1))
        else:
            for i in range(block_size):
                filled_blocks.append(((current_pos + i, 1), fileno))
            fileno += 1
        free_block = not free_block
        current_pos += block_size

    return free_blocks, filled_blocks


def decompress_files(diskmap: list[int]) -> tuple[list[FreeBlock], list[FilledBlock]]:
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


def compact(free_blocks: list[FreeBlock], filled_blocks: list[FilledBlock]) -> None:
    for file_index, ((file_pos, file_size), file_id) in reversed(list(enumerate(filled_blocks))):
        found_free_block = False
        for free_block_index, (free_pos, free_size) in enumerate(free_blocks):
            if free_pos >= file_pos:
                break
            if free_size >= file_size:
                found_free_block = True
                break

        if not found_free_block:
            filled_blocks[file_index] = ((file_pos, file_size), file_id)
        elif free_size == file_size:
            filled_blocks[file_index] = ((free_pos, file_size), file_id)
            del free_blocks[free_block_index]
        else:
            filled_blocks[file_index] = ((free_pos, file_size), file_id)
            del free_blocks[free_block_index]
            free_blocks.insert(free_block_index, (free_pos + file_size, free_size - file_size))


def compute_checksum(disk: list[FilledBlock]) -> int:
    checksum = 0

    for (pos, size), file_id in disk:
        for i in range(pos, pos + size):
            checksum += i * file_id

    return checksum


if __name__ == "__main__":
    main()
