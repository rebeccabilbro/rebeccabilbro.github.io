---
layout: post
title:  Eventually Consistent Distributed Systems
image:
  feature: pepper_crop.png
date:   2018-09-18 19:01
categories: programming
---


[Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency) is a model for consistency for distributed computing, which privileges high availability over perfect consistency at any given moment in time. This model of consistency is helpful in distributed systems that are likely to experience a lot of partitions and faults, and where downstream applications are unlike to cause complex update conflicts. Bayou is an example of a storage system designed to support applications that run on mobile devices via inconsistent network conditions. In this post, I discuss my impressions from reading two of the Bayou papers, ["Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System"](http://zoo.cs.yale.edu/classes/cs422/2013/bib/terry95managing.pdf) and ["Flexible Update Propagation for Weakly Consistent Replication"](https://dl.acm.org/citation.cfm?id=266711).


## Learning from Conflict

One of the strengths of Bayou is that it was built with the perspective that conflict is instructive. Rather than designing a system under perfect "lab conditions," the authors of Bayou created the system in parallel with two applications designed to help identify unique patterns of conflict and inform automated conflict-resolution strategies. Just as actual throughput is useful in proving out such systems, so is actual conflict. In fact, it seems that a not insignificant amount of consideration for the "user experience of conflict" was made in the design of the meeting-scheduling and biblography-entry applications. The applications socialize conflict as both possible and also not catastrophic; worst case you'll get your second or third choice for the room selection, or the system will automatically detect that you and your colleague unknowingly entered the same bibliographic reference into the app. That's all ok; no one freak out!

This struck me as quite a different approach from the ones taken in previous readings, which have tended to be rather conservative in their measures to ensure conflict never, ever occurs in the first place (e.g. locking and leasing). As an application developer, I think that pushing some of the burden of detecting and resolving conflict onto the applications is wise, and also likely to identify behavior that would be difficult to theorize without context.


## Perfection as the Enemy of the Good

A corollary to this conflict-is-ok approach is that certain kinds of conflict shouldn't block progress; it's not necessary for every replica to have the exact correct information at the same time, since most information in a large database has a low probability of collision. The bank balance example they gave was a good one; it shouldn't block a transaction from account A to account B just because it doesn't know for sure exactly how much money is in A, so long as we know that A has at least as much as the transfer amount.

## Safety First

On the other hand, there is one area where the authors seemed to have a much lower tolerance for imperfection and conflict, and this was in the area of security. It occurred to me that few if any of the papers we've read so far in class have even mentioned security, let alone cooked it into the system. I liked the idea that security certificates could be revoked using a regular write procedure, and thereby eventually (hopefully not too slowly) propagated throughout the entire system via pairwise anti-entropy sessions.

This leads me to one of my questions about Bayou, which concerns how well it would perform when certain partitions persist for a long time. The system is designed such that local clusters could theoretically continue to interact in spite of being partitioned from the rest of the network -- what would happen if they were separated for a long time and evolved two very different but internally consistent forks? It seems this state might put a lot of pressure on the system because the majority of writes would remain "tentative" for a very long time. And when finally reunified, many undo operations would be necessary and automated conflict resolution would probably be infeasible.

## The Anti-Entropy Protocol

In the follow-on paper to the original Bayou paper, ["Flexible Update Propagation for Weakly Consistent Replication"](https://dl.acm.org/citation.cfm?id=266711), the authors describe in greater detail the system's anti-entropy protocol. First, there are a few requirements; for instance, Bayou's replicas use an append-only strategy, which means that updates can happen in a single direction without any danger of ambiguous delta resolution problems. Furthermore, the system relies on a version of logical time that implements "a closure constraint on the set of writes known to a server, which we call the prefix-property, ... [that] enables the use of version vectors to compactly represent the set of writes known to a server."  Every replica maintains a logical clock that advances on both new "organic" writes and on anti-entropy "corrective" writes.

These constraints mean that if servers A and B are matched for an anti-entropy session, A can check B's version vector and that will tell A everything it needs to know about what to send to B. There are also some clever optimizations such as, in the case of tentative commits in B that are stable in A, sending only a new commit sequence number rather than the entire commit.

## Garbage Collection and Estranged Replicas

So given the append-only strategy, the problem then becomes how to decide when to retire commits that are stable and obvious to the entire system. As it turns out, estranged replicas can be a problem. This is because if we have to wait for every server to confirm that a commit has been included in its logs, we may be waiting a really long time. And during that time, the logs are going to get really long.

Essentially, Bayou's approach is to be fairly permissive with servers about truncating stable parts of the write-log. If a server is pretty confident that an older chunk of its log has stabilized, it can truncate it. Later, if it determines that there are commits in that truncated log that a new server needs, it can just send its entire database. This obviously isn't ideal, since it will rely on having stable bandwidth for a bit, and the transaction can't be incremental the way that usual anti-entropy sessions are. But they're banking on the fact that replicas won't have to send complete copies of their entire databases too often.

## The Replica Stork

One of the most interesting outcomes of the design and architecture decisions made on Bayou is that it makes it really easy to create new replicas. When you have a single master, you need to talk to master to be allowed to come in and out of the system. With a distributed system like Bayou though, all you have to do is start talking to any of the replicas. This is a very powerful outcome, since it means we can make it easier for the network to recover cheaply and seamlessly. I have a feeling this will come up again in other implementations that we read about!
