---
layout: post
title:  The Pains of Bureaucracy
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-30 17:59
---

Proposed in 1989 and now used in many production systems (e.g. Chubby, Spanner, Ceph, Neo4j) the Paxos algorithm is a method for reaching consensus between replicas in a distributed system. At a very high level, the algorithm is simple; replicas can ask to coordinate, or grant promises to be coordinated; they can broadcast values to be accepted, and either acknowledge or reject those values. Conceptually, this mainly just requires that all replicas know how many total replicas there are in the system, so there's a shared understanding of what it takes to make consensus. If a majority of replicas accept a value, that's consensus, and the value is committed. The algorithm is used by each replica to independently construct and maintain an identical log of values, which can then be used to construct and maintain consistent data across all of the replicas. However, the algorithm is not at all simple in it's execution, as is clear from reading [Paxos Made Live - An Engineering Perspective](https://www.cs.utexas.edu/users/lorenzo/corsi/cs380d/papers/paper2-1.pdf) by Tushar Chandra, Robert Griesemer, and Joshua Redstone. In this post I'll discuss their paper along with the ePaxos paper, which presents a different approach.

## Government in Theory and in Practice

It's hard not to notice the authors' grumpiness at Paxos when reading this paper; they've clearly experienced a great deal of frustration in taking Paxos from theory into practice. In one of the final sections of their paper, they go so far as to call out the fault-tolerance community as a whole, arguing that it has failed to develop tools for implementing and testing algorithms. I wonder, though if this less a function of the community that these ideas have emerged from, and more a function of the time -- 1989 is a pretty long time ago, and it would have been difficult if not impossible for anyone in any field of computer science to be able to anticipate what the authors refer to as "the needs of a real-world system" of today.

It sounds like their main challenge came down to the minutia of governance in a complex system (e.g. master churn, corruption), which to be fair, is probably not what Lamport was really thinking about when he first proposed Paxos. Government is always more complex in practice than in theory.

## Clever Tricks

There were several design choices in the paper that recall earlier papers we've read in class; the "snapshots" are reminiscent of those discussed in the GFS paper and the "landmarks" described in the Elephant system paper, and can also be used to fast-forward lagging replicas to a point where the leading replica can step in with a live log. The offloading of some responsibilities onto the application reminded me of the Bayou and GFS papers. Even the `MultiOp` technique, of bundling several database writes together into a single write (rather than having many smaller writes), recalls in some ways the single-sequential log segment commits of the Log Structured File System.

There were also some very clever techniques that seems novel; I liked the idea of using the simple checksum tool to periodically confirm consistency. I also liked the trick of artificially boosting the sequence numbers for propose messages to help avoid master churn. Finally, I think it was interesting to see where the authors chose *not* to use pure Paxos, such as on reads, where leases can allow master to more efficiently serve read operations purely locally.

## Even More Consensus?

In the [ePaxos paper](https://www.cs.cmu.edu/~dga/papers/epaxos-sosp2013.pdf), Iulian Moraru, David Andersen, and Michael Kaminsky present a different approach to Paxos. The goals of ePaxos are to enable more decentralized activity by allowing more than one leader to function concurrently, and to reduce the ratio of permission-asking messages to action-taking messages.

One result is that they fundamentally change what they mean by a "commit"; in prior readings, a "commit" implies a write to the log; but this is not the case in ePaxos. Because the burden for being allow to "commit" things is so drastically reduced in ePaxos, the notion of a "commit" is also softer than it is for Paxos and for the eventually consistent systems we read about last week. In some sense, commits in Paxos are a kind of buffer, occupying a liminal space where ordering and logic can still be applied before things are permanently executed in the log.

While many other Paxos variants rely upon a stable leader (e.g. Fast Paxos, Generalized Paxos, Multicoordinated Paxos), ePaxos is decentralized. Yet, unlike other decentralized variants, like Mencius (which rotates leaders), ePaxos is able to run more quickly, because it sort of "cheats" by only sending messages to the bare minimum of voters. Kind of the distributed systems version of gerrymandering. The logic here is that for most commands, the probability of conflict is really low; and we don't need everyone to vote every single time if some of the issues aren't relevant to all voters (ironically, this is usually called "elitism", not "egalitarianism").

Though ePaxos passes fewer messages around, they are larger (because they carry more state), and they include some of the information we have encountered in prior readings, such as the `deps` and `seqs`, which are very reminiscent of the dependency chains and causal cuts described in the [Bolt-on Causal Consistency paper](https://rebeccabilbro.github.io/nuts-and-bolts-consistency/).
