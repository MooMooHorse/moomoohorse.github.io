---
layout: post
title:  "Debugfs"
summary: "Dumping Info related to EXT4"
author: moomoohorse
date: '2023-06-29 16:19:35 -0500'
category: ['research']
thumbnail: /assets/img/posts/dbgfs.png
keywords: undergraduate-research
permalink: /blog/dbgfs.png
usemathjax: true22
---

# Dumping Information Related to EXT (2/3/4)

[man page](https://linux.die.net/man/8/debugfs#:~:text=The%20debugfs%20program%20is%20an,e.g%20%2Fdev%2FhdXX) is somewhat helpful.

[this paper](https://www.usenix.org/system/files/conference/atc17/atc17-park.pdf) illustrates some insights about journaling.

[examples](https://www.cs.montana.edu/courses/309/topics/4-disks/debugfs_example.html) of using debugfs.

[wiki](https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout#Journal_.28jbd2.29) for ext4 layout.

[a post](https://stackoverflow.com/questions/11114575/accessing-ext3-ext4-journals) that describes how to access journal.

Thanks to these resources.

## Misconceptions

- when you use `logdump`, the starting blocks is with respect to the journal, not the whole disk.
  
Hence you need to do the following

```bash
dump_extents <8> 
``` 

where `8` is usually the inode number of the journal.

* when the man page mention that the command looks like 
  * `cat filespec`

It actually means that you need to type in `cat filespec` in the debugfs shell.
It also implies that the filespec is something like `<inode>`

* Note that `<>` here does not mean you need to include the value of inode, but the literal string `<inode>`, so you need to type `<` and `>` in the debugfs shell. (Really confusing design).


## Tips

* Use `-R` flag to run a single command and exit.

* You can use arrow keys to navigate through the history of commands.


This post is very short, because I think with these tips, the related resources are enough for you to get started.