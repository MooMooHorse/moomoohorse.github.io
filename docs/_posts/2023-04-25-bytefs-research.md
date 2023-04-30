---
layout: post
title:  "Bytefs : file system built for byte addressable file system"
summary: "My first undergraduate research project"
author: moomoohorse
date: '2023-04-25 18:53:19 -0500'
category: ['filesystem', 'research']
thumbnail: /assets/img/posts/bytefs.png
keywords: bytefs, file-system, undergraduate-research
permalink: /blog/bytefs-research
usemathjax: true
---
# ByteFS File System 

ByteFS is a file system built for byte-addressable SSD. Byte-addressable SSD is an idea inspired directly from at least 3 papers : [Flatflash](https://dl.acm.org/doi/10.1145/3297858.3304061), [2B-SSD](https://ieeexplore.ieee.org/document/8416845), and byte addressable file system such as [NOVA](https://www.usenix.org/conference/fast16/technical-sessions/presentation/xu), [PMFS](https://dl.acm.org/doi/10.1145/2592798.2592814) and [EXT4](https://docs.kernel.org/admin-guide/ext4.html).

I contributed and wrote codes in following aspects :
* Modifying BIO interface in linux kernel to fit our emulator interface.
* Add load to baseline file systems (PMFS, NOVA, F2FS, EXT4) to measure their performance.
* Metadata Cache.
* Page Cache (data cache).

This post contains 2 parts :

1. Technical and high level insights into this project.
2. My idea about my undergraduate research.

This post does NOT represent the viewpoint for my lab [Platform X](https://platformxlab.github.io/). It's just an article to document what I learnt in my undergraduate research.

## Why file system?

Modern development of file systems centers around existing file systems. From what I observed from code base [PMFS](https://github.com/linux-pmfs/pmfs), [NOVA](https://github.com/NVSL/linux-nova), [SplitFS](https://github.com/utsaslab/SplitFS), EXT2, EXT3, EXT4, F2FS... they all build on pre-existing file systems. 

I mean, why not? We use existing code that's tested and structured as our code base. That's normal, right? 

From designing perpespective, I agree. But as an undergraduate student who just starts researching in this field, from implementation perspective, thinking about the concrete implementation while reading code is extremely toxic behavior. In the first 4 months, I can say, that I completely ignore the central idea, why file system?

When I looks at [F2FS](https://www.usenix.org/conference/fast15/technical-sessions/presentation/lee), I can see that, the design of the file system is determined by the underlying storage media. Because flash never overwrites stale data, it utilizes multi-head logging. Because NVMM has low latency on accessing memory, software overhead is non-trivial, hence the list structure and the radix tree in NOVA. Because 2B-SSD, essentially is SSD, with an internal logging and with byte-addressablity, EXT4, F2FS, NOVA, PMFS are all broken against new trade-offs and storage characteristics, hence our motivation of ByteFS. 

![BIO](https://static.lwn.net/images/2017/neil-blocklayer.png)

When I was messing with BIO interface. I read literally workqueues after workqueues, such as [request_queue](https://lwn.net/Articles/736534/). Internally, when I was debugging our 2B SSD emulator, I also went through different queues and was thinking about solutions of optimization strategies by adding new queues. Queues and queuing policies are essential to control the traffics accross different path. **Shortening the critical path is not only the job for the driver writer(like when I was tweaking the emulator), but also one of the most crucial thing to think about when we're designing / implementing file system.** 

Without researching the characteristic of the storage media. You can't write any code about the file system. Hence, I think I wasn't qualified as a researcher at least for the first 4 months because I wasn't thinking of the underlying storage media, our emulator for 2B-SSD(as a baseline, and we made corresponding changes to the interface) and I had no clue what we were trying to design for the file system. 

Another important point is to think about different kinds of workload. This is learnt when I was under the task of testing all baselines as well as our file systems against different workloads like [YCSB](https://github.com/brianfrankcooper/YCSB) and [filebench](https://github.com/filebench/filebench). There are meta-data heavy, data heavy workloads. There are workloads with different R/W ratio and file sizes. Thinking about the kind of workload Bytefs is good at and bad at takes tremendous time for me even when I wasn't designing any features. It's painful but that's essentially the problems we have to deal with.

So, why file system? Essentially we try to execute read / write operations of a set of files. Why does this simple idea need 40k lines of code? 

First, this isn't true. PMFS only has ~6k lines of code, which is fairly light-weighted. With the journaling off (because 2B-SSD internally maintains a log), it's ~3k lines of code. My mini file system (for one of my OS courses) is only 1.5k lines of code and it pretty much did everything a file system can do.

But one common problem these light-weighted file systems are : 
* they are slow
* they are not sophisicated (don't have certain functionalities such as mmap(DIO))

After 6 months, I could say that a file system accelerates generic file operations (read, write, mmap, ...) and lowers the burden of storage media. Every design should aim to do these three objectives. Why three?
* Make it faster by caching and pure software strategies.
* Make it faster by lowering traffic in storage media critical path.
* Leverage the benefits for different file operations under different workload.

## Why Byte FS?

## My Undergraduate Research

### Communication

### Planning and Thinking

### Measure : Engineering and Science

### Designs

### Tools and Setups

### Working with phds

### Time commitment


I know :(  too many blanks are unfilled.

to be continue... 

(It's my final week of the semester so I don't have time for this, but I will come back and try to finish this article)

## Scripts

Run YCSB (no cache)

```bash
#!/bin/bash

workloads=( "workloada" "workloadb" "workloadc" "workloadd" "workloade" "workloadf" )
output_folder="/home/h/output_nocache"

# iterate over the workloads until an unlogged workload is found
for workload in "${workloads[@]}"; do
    log_file="$output_folder/$workload.log"
    if ! [ -f "$log_file" ]; then
        # the log file does not exist, this is an unlogged workload
        touch "$log_file"
        current_workload="$workload"
        break
    fi
done

# if no unlogged workload was found, exit with an error message
if [ -z "$current_workload" ]; then
    echo "All workloads have already been logged."
    exit 1
fi

echo "Running workload $current_workload"

mkfs.ext4 /dev/vdb && mount -t ext4 /dev/vdb dd/ && ./patch_filebench.sh
./Byte_fs/utils/ctrl 906 76800
cd ./YCSB
./bin/ycsb load rocksdb -s -P "workloads/$current_workload" -p rocksdb.dir=/mnt/h/dd -threads 100 
cd ../
./Byte_fs/utils/ctrl 40
cd ./YCSB
./bin/ycsb run rocksdb -s -P "workloads/$current_workload" -p rocksdb.dir=/mnt/h/dd -threads 32 > "$output_folder/$current_workload.log"
echo "======================" >> "$output_folder/$current_workload.log"
cd ../
./Byte_fs/utils/ctrl 42 >> "$output_folder/$current_workload.log"
```

Run YCSB (with cache)

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <workload_name>"
    exit 1
fi

workload="$1"
log_file="/home/h/output/$workload.log"
touch "/home/h/output/$workload.log"

mkfs.ext4 /dev/vdb && mount -t ext4 /dev/vdb dd/ && ./patch_filebench.sh
cd ./YCSB
./bin/ycsb load rocksdb -s -P "workloads/$workload" -p rocksdb.dir=/mnt/h/dd -threads 100 
cd ../
./Byte_fs/utils/ctrl 40
cd ./YCSB
./bin/ycsb run rocksdb -s -P "workloads/$workload" -p rocksdb.dir=/mnt/h/dd -threads 32 > "/home/h/output/$workload.log"
echo "======================" >> "/home/h/output/$workload.log"
cd ../
./Byte_fs/utils/ctrl 42 >> "/home/h/output/$workload.log"
```

Patch filebench

```bash
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```

Module install

```bash
make -j60 modules_install && make install
```

kernel config file is 

[config](../assets/files/config.txt)

[FS-compare](https://www.electronicdesign.com/industrial-automation/article/21804944/whats-the-difference-between-linux-ext-xfs-and-btrfs-filesystems)