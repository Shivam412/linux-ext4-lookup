"""
An extent is a range of contiguous physical blocks, improving
large-file performance and reducing fragmentation. A single extent
in ext4 can map up to 128 MiB of contiguous space with a 4 KiB block size.

resouce: https://www.kernel.org/doc/html/latest/filesystems/ext4/dynamic.html#extent-tree
"""

from __future__ import annotations

# project level imports
from src import Reader

# python inbuilt imports
from dataclasses import dataclass


@dataclass
class ExtentHeader:
    """A class used to represent a Extent's Header.

    Attributes
    ----------
    entries: int
        Number of valid entries following the header.
    depth: int
        Depth of this extent node in the extent tree
    """

    entries: int
    depth: int

    def __repr__(self) -> str:
        return f"ExtentHeader(entries: {self.entries}, depth: {self.depth})\n"

    def new(reader: Reader) -> ExtentHeader:
        """Get a new ExtentHeader."""
        magic = reader.read_int(2, 0x0)
        assert magic == 0xF30A, "Magic number of extend didn't match"

        return ExtentHeader(
            entries=reader.read_int(2, 0x2), depth=reader.read_int(2, 0x6)
        )


@dataclass
class Extent:
    """A class used to represent a Extent, which contains
    information to actual content of the file.

    Attributes
    ----------
    length: int
        Number of blocks covered by extent.
    start: int
        The block number to which this extent points.
    """

    length: int
    start: int

    def __repr__(self) -> str:
        return f"Extent(length={self.length})\n"

    def new(reader: Reader) -> Extent:
        """Get a new Extent."""
        return Extent(
            length=reader.read_int(2, 0x4),
            start=(reader.read_int(2, 0x6) + reader.read_int(4, 0x8)),
        )
