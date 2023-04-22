from __future__ import annotations

# python inbuilt imports
from enum import Enum


class Filetype(Enum):
    Fifo = 0x1000
    CharacterDevice = 0x2000
    Directory = 0x4000
    BlockDevice = 0x6000
    Regular = 0x8000
    SymbolicLink = 0xA000
    Socket = 0xC000

    def from_val(val: int) -> Filetype:
        """"""
        return Filetype(val)
