"""
    Ext4 Block

    ext4 allocates storage space in units of "blocks". A block
    is a group of sectors between 1KiB and 64KiB, and the number
    of sectors must be an integral power of 2.Blocks are in turn
    grouped into larger units called block groups. Block size is
    specified at mkfs time and typically is 4KiB.

    refernce: https://www.kernel.org/doc/html/latest/filesystems/ext4/overview.html#blocks

"""

from __future__ import annotations

# project level imports
from src import Reader, ReaderFactory

# python inbuilt imports
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src import SuperBlock


@dataclass
class BlockGroupDescriptor:
    """A class used to represent a Block-Group Descriptor,
    It contains an offset to a Inode table block in order to access
    the Inodes.

    Attributes
    ----------
    inode_table: int
        soffset to the inode table block.
    SIZE: int (default = 64)
        Block Group descriptor size.
    """

    inode_table: int
    SIZE: int = 64

    def new(reader: Reader) -> BlockGroupDescriptor:
        """Get a new BlockGroupDescriptor"""
        return BlockGroupDescriptor(
            inode_table=reader.read_int(4, 0x8) + reader.read_int(4, 0x28)
        )


@dataclass
class BlockGroupNumber:
    """A class represent the type for a Block Group Number.
    This allow to perform operation like get the Block Group
    Descriptor associated with this number.
    """

    number: int

    def get_descriptor_block(self, sb: SuperBlock, fd: int) -> bytes:
        """Returns the bytes array pointing to the block of BlockGroup Descriptor for this BG number."""
        assert sb.block_size != 1024, "1024 block size not supported"
        gdt_start = sb.block_size  # The superblock takes up 1 block
        offset = gdt_start + self.number * BlockGroupDescriptor.SIZE

        return ReaderFactory.from_file(fd=fd, file_offset=offset).buffer

    def get_blockgroup_descriptor(
        self, sb: SuperBlock, fd: int
    ) -> BlockGroupDescriptor:
        """Get BlockGroup Descriptor for this BG number."""
        reader = ReaderFactory.from_buffer(self.get_descriptor_block(sb, fd))
        return BlockGroupDescriptor.new(reader)
