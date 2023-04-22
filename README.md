# Get into Linux Ext4

Inspired by the [series](https://fasterthanli.me/series/reading-files-the-hard-way/). This project is aim to look how Linux's `Ext4` filesytem works internally using python.
Rather than accessing file using open `syscall`. This will read file directly from the blocks.

> Ext4 currently supported on Linux only, You can used any flavour of linux. Or use Virtual Box with any Linux flavour.
## For Running the example, replace the filename you get by running
```
$ df /
------------------------------------------------------------------
Filesystem     1K-blocks    Used      Available  Use%  Mounted on
/dev/ubuntu    11758760     8675048   2464604    78%   /
------------------------------------------------------------------
```

### Then using the following command
```
$ chmod +x main.py
# opening dev file required sudo access.
$ sudo ./main.py
```

references: https://www.kernel.org/doc/html/latest/filesystems/ext4/