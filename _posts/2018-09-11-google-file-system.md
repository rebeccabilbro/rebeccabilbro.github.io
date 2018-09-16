---
layout: post
title:  Everything Old is New Again
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-11 20:26
---

How does Google work under the hood? I remember first reading about Google's [PageRank algorithm](https://en.wikipedia.org/wiki/PageRank) and just marveling at how innovative and elegant it was. I suppose that I have come to expect such greatness from a company with seemingly unlimited resources. For this reason, reading the [Google File System paper](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf) came as a bit of a surprise to me. Although Ghemawat et al. frame GFS as radically different from prior implementations of file systems, I was more surprised by its resemblances to past examples than I was by its novelties. In this post I discuss my reactions from reading the paper.

## Everything Old is New Again

As Helland argues in ["Immutability Changes Everything"](https://rebeccabilbro.github.io/immutability-helland/), "the truth is the log"; and the authors of GFS take an append-only approach, where the operation log is "not only the only persistent record of metadata, but also...a logical time line that defines the order of concurrent operations" -- this ends up being essential to GFS because the expectation from the outset is that there will be concurrent operations. Like the [log-structured file system paper](https://rebeccabilbro.github.io/log-structured-filesystem/), GFS uses fixed-size chunks for blocking files (though these are admitted enormous in GFS), and also adopts a batchwise approach to flushing logs, which is similar to the log segments in LSF. I also found the notion of a GFS system "snapshot" quite similar to the "landmarks" described in the [Elephant system paper](https://rebeccabilbro.github.io/elephant-file-system/).

## Everything That Can Go Wrong Will Go Wrong

One of the things that makes GFS so effective is the assumptions it makes going in. For instance, file sizes will follow a Zipfian distribution, but the tail will be mostly small files, not big ones. Moreover, most hardware in a networked file system is cheap and expendable, so that it will fail should be taken for granted. GFS's solution is effective delegation from the master to it's chunkservers. One of the unique qualities of GFS from my perspective was how little master is actually responsible for; it maintains the log and grants "leases" to it's delegates to allow them temporary mutation rights, and it sends out periodic "heartbeats" to detect when a chunkserver has gone stale... but that's basically all. Master doesn't persist the location of all its chunkservers, and stores only a very tiny fraction of information corresponding to each chunk of file in the system. Moreover, master has replicas, to which it delegates much of the work of managing chunk mutation.

## Multiclient Concurrent Appends

I was very interested in the description of "record appends," which are how GFS handles multiclient concurrent appends. The strategy is that when multiple users are appending to a file, we add each append atomically and use XXL offsets to ensure that edits don't collide, while also preserving each writer's contribution. The extra padding can then be dealt with via the reader, which can ignore big empty blocks and identify and handle possible duplicates - neat trick!

## Mushrooms or Trees

As we've been working on our implementations of an in-memory file system, we have conceived of file systems as trees; directories and files contained within other directories, within other directories, etc. Therefore one of the more striking realizations about GFS is that it is not a tree; "Unlike many traditional file systems," the authors explain, "GFS does not have a per-directory data structure that lists all the files in that directory... there is no 'directory' or inode-like data structure to be protected from modification." This is fascinating, calling to mind not a tree or even a forest, but something more akin to mushroom colonies! Trees take a long time to grow and require a lot of resources; mushrooms are small and cheap and can be re-replicated overnight.
