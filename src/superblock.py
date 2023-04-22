"""
The superblock records various information about the enclosing filesystem,
such as block counts, inode counts, supported features, maintenance information, and more.

refernce: https://www.kernel.org/doc/html/latest/filesystems/ext4/globals.html#super-block

"""
from __future__ import annotations

# project level imports
from src import Reader

# python inbuilt imports
from dataclasses import dataclass


@dataclass
class SuperBlock:
    """A class used to represent a SuperBlock.
    Attributes
    ----------
    magic: int
        Magic signature, 0xEF53.
    block_size: int
        Block size.
    blocks_per_group: int
        Blocks per group.
    inodes_per_group: int
        Inodes per group.
    inode_size: int
        Size of inode structure, in bytes.
    """

    magic: int
    block_size: int
    blocks_per_group: int
    inodes_per_group: int
    inode_size: int

    def __repr__(self) -> str:
        return f"""SuperBlock(
    magic number: {self.magic:x}
    block size: {self.block_size}
    blocks per group: {self.blocks_per_group}
    inodes per group: {self.inodes_per_group}
    inode size: {self.inode_size}
)
    """

    def new(reader: Reader) -> SuperBlock:
        """Returns a new super block"""
        return SuperBlock(
            magic=reader.read_int(2, 0x38),
            block_size=1 << (10 + reader.read_int(4, 0x18)),
            blocks_per_group=reader.read_int(4, 0x20),
            inodes_per_group=reader.read_int(4, 0x28),
            inode_size=reader.read_int(2, 0x58),
        )
