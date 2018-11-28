---
layout: post
title:  Trust and Consistency in Distributed Systems
image:
  feature: pepper_crop.png
date:   2018-11-25 17:40
tags:   class_readings
---

Although the [Practical Byzantine Fault Tolerance paper](http://pmg.csail.mit.edu/papers/osdi99.pdf) presented an optimization of Lamport et al's algorithm that worked in asynchronous environments with only a small amount of added latency, it made a fundamental assumption that at least *some* servers would be trustworthy. In the [SUNDR](https://www.usenix.org/legacy/events/osdi04/tech/full_papers/li_j/li_j.pdf) and [SPORC](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Feldman.pdf) papers, the authors present an alternate approach to securing data in distributed systems, assuming that perhaps no servers will be trusted, and instead allocating trust at a much more granular file/directory level. 

## SUNDR

SUNDR provides two types of security. First, SUNDR's block server stores and retrieves blocks using hashes and user keys, making unauthorized activity immediately recognizable and pretty difficult to even do in the first place. When users create a new file system, they create a pair of public and private keys; the server only gets the public half, meaning that no one has access to everything. Secondly, SUNDR's consistency server stores version vectors, which can be used to (though not immediately, still eventually) expose any ordering failures (via "fork consistency").

The implementation requires a few new data structures, first `i-handles`, which are a sort of aggregated hash of the hashes of all the files that a single user or group has access to. As files are created and modified, `i-handles` are updated and passed around in messages called `version structures`.  The `version structure list` keeps track of the accessible files for every user and group. What if two users want to modify a directory (to which both have access)? SUNDR enables concurrency by introducing `pending version lists`, which are communicated between servers using RPCs, and which allow a total order of operations (and expose any forking attacks as ordering failures). 

This means that we can detect attacks (either when a file/dir mod is signed by someone who doesn't have permission, or when we identify concurrent operations resulting from a forking attack), but SUNDR doesn't give us a way to resolve those attacks. In addition, though I can see how SUNDRs block server and user/content hashing would expose illegal writes, it's not clear to me that it would reliably identify unauthorized reads.

## SPORC

SPORC takes up where SUNDR left off, and ends up feeling like the more approachable, developer-friendly version of the incredibly dense SUNDR. SPORC is focused on addressing the kinds of issues that applications developers are going to encounter in practice when building a group collaboration app on top of an untrusted distributed file system. For instance, SPORC gives users a framework not only for detecting misbehavior, but also for addressing it, by switching to a new server and recovering an untainted, consistent state of their files and directories. It also provides ways to conveniently toggle on and off permissions at the user level, so that the changes will go into effect immediately, even in the face of concurrency.

In addition, SPORC implements deeper optimizations by combining operational transformation with fork consistency to provide more availability to users without pessimistic locking (and while still achieving causal consistency). While SUNDR required users to pre-declare fetch and modify operations before being allowed to move forward, SPORC allows for optimistic local updates.

One of the questions I had comes as a follow-on to SUNDR, which used a consistency server to store version vectors, enabling the eventual detection of forking attacks -- my question about SPORC concerns just how eventual this detection would be?