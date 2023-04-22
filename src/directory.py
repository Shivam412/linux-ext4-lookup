"""
In an ext4 filesystem, a directory is more or less a flat file that maps an arbitrary
byte string (usually ASCII) to an inode number on the filesystem. There can be many
directory entries across the filesystem that reference the same inode number–these are
known as hard links.

refernce: https://www.kernel.org/doc/html/latest/filesystems/ext4/dynamic.html#directory-entries
"""
from __future__ import annotations

# project level imports
from src import Reader

# python inbuilt imports
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src import InodeNumber


@dataclass
class DirectoryEntry:
    """A class used to represent the Directory Entry fot the ext4 FS.

    Attributes
    ----------
    length: int
        Length of this directory entry.
    inode_no: InodeNumber
        Number of the inode that this directory entry points to.
    name: str
        File name.
    """

    length: int
    inode_no: InodeNumber
    name: str

    def new(reader: Reader) -> DirectoryEntry:
        """Get a new Directory Entry."""
        from src import InodeNumber

        name_len = reader.read_int(1, 0x6)
        return DirectoryEntry(
            length=reader.read_int(2, 0x4),
            inode_no=InodeNumber(reader.read_int(4, 0x0)),
            name=reader.get_byte_slice(name_len, 0x8).decode(
                "utf-8",
                "replace",
            ),
        )
