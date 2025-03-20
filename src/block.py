import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    HEADING = "heading"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def check_block_sequence(block, designator):
    for line in block.strip().split("\n"):
        if line[0 : len(designator)] == designator:
            continue
        return False
    return True


def check_block_ordered_list(block):
    scratch = block.strip().split("\n")
    count = 1
    for line in scratch:
        if line[0 : len(str(count)) + 2] == f"{count}. ":
            count += 1
            continue
        return False
    return True


def block_to_block_type(block):
    print(block)
    if re.match(r"^#{1,6}\ ", block):
        return BlockType.HEADING

    if re.match(r"^```.+```$", block.strip()):
        return BlockType.CODE

    if check_block_sequence(block, ">"):
        return BlockType.QUOTE

    if check_block_sequence(block, "- "):
        return BlockType.UNORDERED_LIST

    if check_block_ordered_list(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
