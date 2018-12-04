---
layout: post
title:  Distributed Hide and Seek
image:
  feature: pepper_crop.png
date:   2018-12-03 18:56
tags:   class_readings
---

In this post we'll explore [Obladi](https://www.cs.cornell.edu/~ethan/papers/obladi.pdf), a distributed system that aims to deliver high performance transactions while masking access patterns.

## Obladi
In theory, replication is great because it increases availability. However, replicating some data, like PII increases the risk of exposure. 

Obladi's solution is to mask access patterns, hiding the frequency of access to keys, in addition to their values. Unfortunately, ACID transactions often make pretty heavy use of these accesses under the hood to reliably order reads and writes. 

Obladi is built on top of ["oblivious RAM" (ORAM)](https://dl.acm.org/citation.cfm?id=28416), a probabilistic approach to RAM that ensures accesses are uniformly distributed across memory locations (for both reads and writes, I think). Obladi accesses to distributed storage cannot be statistically distinguished by an adversary from purely random accesses.

How? Obladi uses fixed-size epochs to buffer the execution of batches of committed transactions. The buffering delays system-wide visibility until the transactions can be executed at a trusted proxy. Execution at the trusted server means that we can have our cake and eat it too; the fault tolerance that comes with leveraging a network of untrusted servers *without* exposing private values or frequently accessed keys. The batching (as we've seen in previous readings) makes the execution of lots of little transactions much more efficient than they would be executed separately.

What's cool is that Obladi manages the above without sacrificing on consistency, though recovery is admittedly somewhat of a heavier lift, requiring write-ahead logging (i.e. commits only durable at the end of epochs; abort transactions on failure) and the COW technique [shadow paging](https://en.wikipedia.org/wiki/Shadow_paging) (i.e. we allocate a "shadow" page when a page is going to be modified so we can avoid in-place updates).

The separation of concerns is very appealing, particularly for a field like medicine, education, or other public institutions where a lot of PII data is going to be stored and modified across many machines. Obladi essentially uncouples the specifics of the (potentially sensitive) transactions and the patterns of writes and reads that could be used by bad actors to extrapolate diagnoses, physical locations, dates of birth, email addresses, etc.
