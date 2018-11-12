---
layout: post
title:  The Shared Log Abstraction
image:
  feature: pepper_crop.png
date:   2018-11-11 12:52
tags:   class_readings
---


The evolution in thought around consensus algorithms, with Paxos and variants like Multi-Paxos, ePaxos, and the alternative Raft, share the fundamental characteristic of imagining the replica as more than just storage. The metaphors that are used in those papers include things like democracy and war, and cast replicas as entities in a (sometimes more, sometimes less contentious) exchange with each other. Sometimes there is an elected leader, sometimes an appointed leader, and sometimes each member of the group shares equally in the weight of governance. It is interesting, therefore, to read papers such as FAWN, Corfu, and Tango, which see replicas as much more passive participants in the overall replication process. 

## CORFU 

In Corfu, the individual units of replication are flash memory units, passive storage devices that have no responsibility for consensus logic or replication protocols. Instead, the brunt of coordination is pushed to the client side (though it's worth noting here that the "clients" in this case are imagined to be other infrastructure layers, like key-value stores and state machine replication libraries, such as the CORFUStore and CORFU-SMR described at the end of the paper). 

CORFU clients maintain local "projections" of ranges of log segments, which enable them to map between memory pointers (e.g. logical addresses) and physical flash pages. As in the Log Structured File System paper, the pointers are contained in a single log, though in CORFU, the log is distributed across clusters of flash units. Unlike in FAWN (which had multiple logs without a total ordering across), the single CORFU log is distributed across flash drives and appended to by multiple clients. Clients append to the tail of the log (here, vying for the tail in a manner reminiscent of replica leader election in Paxos), then kick off instances of chain replication, so that each flash-based replica gets updated in a predefined order.

The rest of the responsibility of the system rests on the sequencer node, which is responsible for passing out monotonically increasing log positions to clients upon request. These "tokens" give clients append permission, and crashes manifest as "holes" in the log, which are addressed by clients who fill them in with junk (which later signals to the garbage collector). It was not clear to me how clients attempting to fill holes with legitimate writes and those filling them with junk markers would not sometimes collide. I was also not totally clear on the protocol for reconfiguration, which was apparently inspired by Vertical Paxos, with which I am not yet familiar.

## Tango

Having been built by the same team as CORFU, and built atop CORFU's shared log abstraction, there is unsurprisingly a large amount of overlap between Tango and CORFU. However, while the focus of the CORFU paper is mainly on demonstrating how to achieve a distributed log on flash memory (and the benefits thereof, like lower costs and super fast reads), the main focus of Tango is on the nuts and bolts of decentralizing metadata storage (how the transactions work, how to ensure correctness, consistency, etc). 

As with CORFU, Tango offloads the brunt of the work to the (infrastructure-layer) clients and the sequencer node. Tango leverages the distributed CORFU log to provide consistency, durability, history, and elasticity. It adds to that transactional atomicity and isolation, and addresses the "playback bottleneck" which would otherwise limit the speed with which any single client could reconstitute the full log from the many separate projections (ranges of log segments). In the Log Structured File System paper, Ousterhout and Rosenblum gave us a way to recompose a file using the "recipe" of it's inode, a mapping between file metadata and data blocks; as blocks were modified, the inode recipe changed. In Tango, objects can be reconstituted using a stream, which can skip through the log to find only the relevant ingredients. The result is highly available metadata that is still strongly consistent.

This means that transactions that modify a single object are pretty straightforward, however, we must also consider the Alice-and-Bob examples, where a single transaction increases one bank account and decreases another. Multi-object transactions go into the log just like single-object transactions, but get broadcast to more than one object stream. What if the updates involve objects that a client doesn't have the metadata for? In CalvinFS, this was solved by having the local metadata broadcast to all participating replicas, and only the relevant updates applied locally. This is tougher to deal with in Tango, since clients don't directly communicate with RPCs (e.g. the way they do in the ePaxos-inspired system we are implementing). The solution is to limit Tango's functionalities to those that limit conflict resolution overhead.

One of the strategies that Tango espouses is Optimistic Concurrency Control, essentially relaxing the implied permanence of a commit, since a commit can be committed to the log speculatively and later undone if it is determined to conflict.