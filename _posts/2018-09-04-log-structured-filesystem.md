---
layout: post
title:  A Log-Structured Filesystem
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-04 17:38
---

Conventional file systems treat storage spatially, and when we as users want to change the files, the system seeks to the correct location and makes our changes in-place. In 1991, John K. Ousterhout and Mendel Rosenblum published a paper called "The Design and Implementation of a Log-Structured File System," which proposed a new way of treating memory storage. This post contains my notes and reactions from reading the paper.

## An Append-only Approach
My first take away is that this paper is a very interesting follow-on to [reading Pat Helland’s "Immutability Changes Everything,"](https://rebeccabilbro.github.io/immutability-helland/) which argues that immutability means that data inside a transactional database should not change — except to accumulate. At a very high level, what Ousterhout and Rosenblum seem to be proposing is an append-only filesystem (with some optimizations for disk space management).

Conventional file systems treat storage spatially; a file is conceptualized a discrete thing that has a specific and unique address on disk. So what if we want to modify a file? In this case, we have an inode lookup that tells us the memory address of that file on disk. When we as users want to change our file, the system uses the inode lookup to seek to the correct location and makes our changes in-place. But as Ousterhout and Rosenblum point out (in 1991!), we're starting to run more intensive processes on our computers, and while RAM is increasing exponentially, the speed of seeking to the correct file (aka access time) is constrained by the speed at which physical disks can spin (this is obviously before you could buy flash drives for a few bucks and expect your new laptop to come standard with SSD).

Ousterhout and Rosenblum's solution relies on us rethinking what a "file" is. If a file is just a bunch of chunks (blocks) of data, when we update that file, we only need to update the blocks that are changed. Moreover, if we think of inodes not as disk addresses anymore, but as pointers to the blocks that comprise a file, we can reconstruct a file using the inode. Now with this idea of files as blocks that can be reconstituted via an inode, we can rethink how we structure our filesystems so that they don't require us to seek to a specific place on disk whenever a file update is needed. In short, the entire filesystem becomes an append-only log, which we hold in memory in segments, which we periodically write to disk sequentially.

This all seems quite clever and elegant! The approach does get a bit more complex, though, when we have to determine how to recover memory from blocks that correspond to files that have been deleted, or to chunks of files that have been rewritten and are thus superseded by new blocks. In other words, what do we do with blocks that are no longer referenced by any inodes? Well, we can compile a map of active inodes (inode map), and from those we can follow the references to inodes and to blocks that are active; inactive blocks can be recycled. Ousterhout and Rosenblum's approach finds log segments with sufficiently many inactive blocks, compresses those logs into only active blocks, and then re-writes them to disk as a new log segment. They refer to this as "segment cleaning."

Quite a lot of the paper is devoted to the experiments and optimizations Ousterhout and Rosenblum performed to test and tune different segment cleaning policies; they finally land on an optimization that divides files into two groups - a small "hot" group and a large "cold" group - named for how often they are likely to be used and cleaned. The first experiments with this differential approach failed to be performant because the large cold group took a long time to reach the cleaning threshold. The final compromise was a policy that set different cleaning thresholds for the hot and cold groups, which resulted in significantly higher disk capacity usage! I was curious about other ways that the segment cleaning policy could be set -- for instance, could we train a machine learning model that would learn features of the files (e.g. filetype, file contents, metadata like historic access patterns) most and least likely to be rewritten/deleted (e.g. an image file is less likely to be updated than a text file or a spreadsheet)?

I was also a bit curious about how a log would be distributed to many VMs, and how best to maintain consistency of the copies of the log as changes are made to many different copies on many different replicas. Would there be latency issues? Inconsistencies? Do we keep a single master log that serves as a source of truth? Do we pass full logs between replicas to ensure consistency, or just the checkpoints?


## Further Reading

 - [Original Paper](https://web.stanford.edu/~ouster/cgi-bin/papers/lfs.pdf)
 - [What is a Filesystem?](https://rebeccabilbro.github.io/what-is-a-file-system/)
 - [LSF Notes from Cornell](http://www.cs.cornell.edu/courses/cs4410/2015su/lectures/lec20-lfs.html)
 - [Wikipedia entry on LSF](https://en.wikipedia.org/wiki/Log-structured_file_system)
 - [LSF Lecture by David Evans](https://www.youtube.com/watch?v=KTCkW_6zz2k)
 - [LSF Preliminaries from Georgia Tech](https://www.youtube.com/watch?v=TYqBtau0bYw)
