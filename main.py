#!/usr/bin/python3

# python inbuilt imports
from src import ReaderFactory
from src import SuperBlock
from src import InodeNumber


def main() -> None:
    with open("/dev/mapper/ubuntu--vg-ubuntu--lv", "rb") as file:
        fd = file.fileno()
        super_block = SuperBlock.new(ReaderFactory.from_file(fd))
        print(super_block)

        root_inode = InodeNumber(2).get_inode(super_block, fd)
        print(root_inode)

        etc_inode = root_inode.get_child("etc", super_block, fd).get_inode(
            super_block, fd
        )
        print(etc_inode)

        host_inode = etc_inode.get_child("hosts", super_block, fd).get_inode(
            super_block, fd
        )
        hosts_data = host_inode.get_inode_data_block(super_block, 0, fd)
        print("---------------------------------------------------------------")
        print(hosts_data.decode("utf-8", "replace"))


if __name__ == "__main__":
    main()
