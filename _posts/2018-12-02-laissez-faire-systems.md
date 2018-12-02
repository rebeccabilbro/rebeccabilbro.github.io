---
layout: post
title:  Laissez-Faire in Distributed Systems
image:
  feature: pepper_crop.png
date:   2018-12-02 16:42
tags:   class_readings
---

What do we want? Distribution with strong consistency! When do we want it? Faster than the speed of consistency protocols! Well, according to the traditional wisdom, that puts us in a bit of a bind. In this week's papers on Eris and Fuzzylog, we see two different takes on distribution that attempt to give us what we want in return for relaxing some of the things (namely, consistency at the log replication layer and single total ordering) we always thought we needed.

## Eris

[Eris](https://syslab.cs.washington.edu/papers/eris-sosp17.pdf) is a system for high-performance distributed transaction processing, named after the Greek goddess of discord. We get it, we get it -- coordination protocols are *so* painful that we're eschewing the governance metaphors altogether and throwing our lot in with the bad guys. 

Eris clients send transactions directly to replicas, which use a quorum based protocol with a designated learner replica whose job it is to execute transactions synchronously (while the others just log it for asynchronous execution). However, Eris is unique in that it can execute independent transactions without any coordination, leveraging a sequencer (recall [CORFU and Tango](https://rebeccabilbro.github.io/the-shared-log-abstraction/)) that operates at the datacenter layer. This enables the system to provide uniquely high throughput and low latency distributed transactions. 

With Eris, datacenters use multi-stamps to order independent transactions (e.g. focused, atomic updates across multiple shards) via multi-sequencing, a network-level abstraction that ensures every replica in the system gets the update message in a consistent order. More complex transactions (i.e. ones that depend on non-local reads in order to write) are implemented in two stages, with a preliminary transaction that gathers all the read dependencies, and a follow-up transaction that wraps up the rest.

I liked the idea of combining the strengths of the network together with those of the application layer. For instance, in Eris, a failure coordinator is used for recovery, guarding against lost messages and delivery errors. In the case of a network failure, when a replica misses a message, the failure coordinator pings the other replicas to get the missing transaction and sends it to the replicas who need it. If it can't get a copy from the other replicas, it tells all of the replicas to drop that transaction.

## Dapple

[Dapple](https://www.usenix.org/system/files/osdi18-lockerman.pdf) is a system that stores a distributed shared log abstraction that calls to mind CORFU and Tango, but that is *partially ordered* and relaxes the requirement for system-wide total order. In so doing, it boasts linear scalability, causal+ consistency (as described in the [COPS paper](https://rebeccabilbro.github.io/slightly-more-consistent/)), and network partition tolerance, without increasing code complexity or chucking convenient system semantics. 

As we have seen in these prior readings, the single total ordering of the shared log abstraction is a powerful and convenient thing to build on top of; offering ACID transactions and a simple, coherent application layer. That's why people implement Paxos & it's variants even when it's very painful. As we've seen from our project to implement ePaxos, effectuating a system that has a single total ordering is quite difficult to do. 

We have also seen some alternative approaches, such as in CORFU and Tango, with the independent sequencer (picture the ticket dispenser at the deli, but for slots in the log) and sneaky junk-filling routines used to impose that total ordering. However, we began to suspect that it might be difficult to scale that sequencer model beyond rather small clusters, hypothesizing penalities as networks became more physically dispersed, and bandwidth became less reliable.

Fuzzylog takes a new path, weakening consistency across shards that are very geographically dispersed so that regions won't require the aggressive coordination of something like a sequencer. But it shards data in such a way as to supports atomicity across shards while also allowing for concurrent updates at different shards.

How do they do this? Well, it means that the log isn't a line anymore, it's a graph. The nodes (essentially blocks/batches of operations, I think) of the directed, acyclic graph log are composed of chains of commits related by geographic locality, and color-coded by region. The regional subgraphs are not disjoint, they have edges that denote causality (causal+) between operations to a single color across regions, and each region is aware of the nodes in every other region (but might have a stale view of them).

From the experimental results, I got the impression there would be a bit of a sweet spot in terms of the amount of sharding with Fuzzylog. On the one hand, not enough partitioning led to overloaded servers, while on the other hand, instincts suggest that after sharding across too many distant regions, the staleness of local copies of remote data might start to impact the user experience of the application, particularly if we expect geographically dispersed users to be interacting much with each other's data.