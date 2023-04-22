from __future__ import annotations

# python inbuilt imports
import os

FILE_BUFFER_SIZE = 128
SUPER_BLOCK_OFFSET = 1024


class Reader:
    """A class used to represent a Reader thats read data from a buffer.

    Attributes
    ----------
    buffer: bytes
        Byte array to read from.
    offset: int (default = 0)
        Add this offset to the position while reading data.
    """

    def __init__(self, buffer: bytes, offset: int = 0) -> None:
        self.buffer = buffer
        self.offset = offset

    def read_int(self, n: int, pos: int, byteorder="little") -> int:
        """Read n bytes from the given position and convert them to int."""
        return int.from_bytes(
            self.buffer[pos + self.offset : pos + self.offset + n],
            byteorder=byteorder,
        )

    def get_byte_slice(
        self,
        n: int,
        pos: int,
    ) -> bytes:
        """Returns slice from a bytes"""
        return self.buffer[pos + self.offset : pos + self.offset + n]


class ReaderFactory:
    """Get Reader based on a file or a buffer."""

    @classmethod
    def from_buffer(cls, buffer: bytes, offset: int = 0) -> Reader:
        """Get Reader from a given buffer."""
        return Reader(buffer, offset)

    @classmethod
    def from_file(
        cls,
        fd: int,
        size: int = FILE_BUFFER_SIZE,
        file_offset: int = SUPER_BLOCK_OFFSET,
        offset: int = 0,
    ) -> Reader:
        """Get Reader from a given file and file offset,
        The file offset is the offset after which bytes will be read."""
        return Reader(os.pread(fd, size, file_offset), offset)
