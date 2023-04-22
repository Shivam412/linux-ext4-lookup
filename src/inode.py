"""
In a regular UNIX filesystem, the inode stores all the metadata pertaining to the file
(time stamps, block maps, extended attributes, etc), not the directory entry.
To find the information associated with a file, one must traverse the directory files
to find the directory entry associated with a file, then load the inode to find the
metadata for that file.

refernce: https://www.kernel.org/doc/html/latest/filesystems/ext4/dynamic.html#index-nodes
"""

from __future__ import annotations

# project level imports
from src import (
    Reader,
    ReaderFactory,
    BlockGroupNumber,
    Filetype,
    ExtentHeader,
    Extent,
    DirectoryEntry,
)

# python inbuilt imports
from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src import SuperBlock


@dataclass
class INode:
    """A class used to represent a Inode.

    Attributes
    ----------
    mode: int
        The mode of the Inode
    size: int
        The size of the Inode
    block: bytes
       Block map or extent tree
    """

    mode: int
    size: int
    block: bytes

    def __repr__(self) -> str:
        return f"({self.get_filetype()}) | Node(mode={self.mode:o}, size={self.size})\n"

    def new(reader: Reader) -> INode:
        """Get a new INode"""
        return INode(
            mode=reader.read_int(2, 0x0),
            size=reader.read_int(4, 0x4) + reader.read_int(4, 0x6C),
            block=reader.get_byte_slice(60, 0x28),
        )

    def get_filetype(self) -> Filetype:
        """Get the file type from the mode"""
        return Filetype.from_val(self.mode & 0xF000)

    def get_inode_data_count(self) -> int:
        """Get this Inode's data count, It may happend data presented in more than one Block,
        In that case get more data using the extent information.
        """
        extent_header = ExtentHeader.new(ReaderFactory.from_buffer(self.block))
        assert extent_header.depth == 0, "Currently only depth 0 is supported"
        return extent_header.entries

    def get_inode_data_block(self, sb: SuperBlock, index: int, fd: int) -> bytes:
        """Get this INode's data block, where all information is presented"""
        extent_header = ExtentHeader.new(ReaderFactory.from_buffer(self.block))

        assert extent_header.depth == 0, "Currently only depth 0 is supported"
        assert extent_header.entries > index, "entries should be more than index"

        # To get the extent which is index dependent.
        extent = Extent.new(
            ReaderFactory.from_buffer(self.block, offset=12 * (index + 1))
        )
        assert extent.length == 1, "data from ext length 1 is supported."

        offset = extent.start * sb.block_size
        length = extent.length * sb.block_size

        return ReaderFactory.from_file(fd=fd, size=length, file_offset=offset).buffer

    def dir_entries(self, sb: SuperBlock, fd: int) -> List[DirectoryEntry]:
        """Get Directory entries for this INode block has information about."""

        ls = []

        for index in range(self.get_inode_data_count()):
            block = self.get_inode_data_block(sb, index, fd)
            block_size = len(block)
            offset = 0

            while offset < block_size:
                entry = DirectoryEntry.new(ReaderFactory.from_buffer(block, offset))
                if entry.inode_no.number == 0:
                    break
                offset += entry.length
                ls.append(entry)

        return ls

    def get_child(self, name: str, sb: SuperBlock, fd: int) -> Optional[InodeNumber]:
        """Search a child is presented in the INode's directory entries."""
        entries = self.dir_entries(sb, fd)
        return filter(lambda d: d.name == name, entries).__next__().inode_no


@dataclass
class InodeNumber:
    """A class represent the Inode's Number, which allows to perform operation
      directly for the give Inode number.

    Attributes
    ----------
    number: int
        This represent the Inode's number.

    """

    number: int

    def blockgroup_number(self, sb: SuperBlock) -> BlockGroupNumber:
        """Get the Block Group number this Inode belongs to."""
        number = (self.number - 1) // sb.inodes_per_group
        return BlockGroupNumber(number)

    def get_inode_block(self, sb: SuperBlock, fd: int) -> bytes:
        """Get the Inode block buffer for the give Inode number."""
        descriptor = self.blockgroup_number(sb).get_blockgroup_descriptor(sb, fd)
        table_offset = descriptor.inode_table * sb.block_size
        idx_in_table = (self.number - 1) % sb.inodes_per_group
        inode_offset = table_offset + sb.inode_size * idx_in_table
        return ReaderFactory.from_file(fd=fd, file_offset=inode_offset).buffer

    def get_inode(self, sb: SuperBlock, fd: int) -> INode:
        """Get Inode for this Inode number."""
        reader = ReaderFactory.from_buffer(self.get_inode_block(sb, fd))
        return INode.new(reader)
