---
layout: post
title:  A Low-Bandwidth Network Filesystem
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-04 19:24
---

A network file system (NFS) is a protocol for writing distributed file systems. It gives me (for example) and my co-worker a way to access the same networked files from our local machines. While this is convenient, it can cause availability (lag) issues for really interactive applications. This post contains my notes from reading "A Low-bandwidth Network File System," by Muthitacharoen, Chen, and Mazieres, who present a solution to this problem.

## First, What is a Network Filesystem?

A network file system (NFS) is a protocol for writing distributed file systems protocol. It gives me (for example) and my co-worker a way to access the same files from our local machines. Just as a local userspace filesystem daemon provides data and metadata of the filesystem, NFS daemons are programs that run and make data available to users across the network. The server administrator specifies which files and directories are publicly available. My colleague and I make requests to the server to access a certain mount point, we are validated by the security protocol, and then we both have access. That's very convenient!

## Why Low-Bandwidth?

Let's say I make some updates to a file and re-save it. The next day, right before the big presentation, my colleague goes in and fixes a typo (thanks Dave!). But when I go to open up the file, it takes a long time. My machine is making the exact same request it made yesterday for what is essentially the exact same file, with only one word changed. That's not very efficient.

In "A Low-bandwidth Network File System," Muthitacharoen, Chen, and Mazieres present a solution to this problem. The Low-bandwidth Network File System (LBFS), breaks files into chunks not unlike the blocks proposed in the [Log-Structured Filesystem paper](https://rebeccabilbro.github.io/log-structured-filesystem/). That way, when a chunk of a file is changed, my machine can compare the version of the file that I have and the current version on the server, and only request the updated chunk, which will significantly decrease the bandwidth required to get updates. The chunks can be uniquely identified by their hashes. This is similar (I think) to how Git works.

One of the unique ideas in the Muthitacharoen, et al. paper is that it is better to used variable-sized chunks than fixed-size blocks (though they do set a lower and upper bound to ensure that we don't break a file down into single words, say, or into a single massive chunk).

While this variable-sized chunking can lead to some problems, as the authors suggest, the worst case scenario "is that LBFS will perform no better than an ordinary file system." But is that really true? But is that really true?

## Consistency

What happens if my colleague and I edit the file at the same time (or nearly the same time)? Whose changes stick? The LBFS authors address this possibility by defaulting to atomicity. When I modify a file, it isn't actually written back to the server until I close it. If my computer crashes while I'm working on a file, my changes will all go away, and when my colleague requests the file later, he'll see the old version without any of my changes. If he and I write to the same file at the same time, the last one of us to close the file "wins", meaning that if Dave closes the file after me, his changes will overwrite mine.

While the LBFS solution is attractive in the sense that it will produce a much more responsive experience (particularly convenient if I'm more likely to be reading than writing), it seems a bit conservative. I also wonder if it will become increasingly problematic as a file system is increasingly geographically distributed?


## Further Reading

 - [Original paper](https://pdos.csail.mit.edu/papers/lbfs:sosp01/lbfs.pdf)
 - [Wikipedia entry](https://it.wikipedia.org/wiki/Low_Bandwidth_Network_Filesystem)
 - [A Low-Bandwidth Network File System by Joseph Thompson](https://slideplayer.com/slide/8915392/)
