---
layout: post
title:  Riddles of Consensus
image:
  feature: pepper_crop.png
date:   2018-11-17 12:35
tags:   class_readings
---

The Byzantine General's Problem, introduced in [Lamport et al's 1982 paper](https://lamport.azurewebsites.net/pubs/byz.pdf), presented one of the key problems in distributed consensus; namely that in a distributed system, we can't always trust other system components. The solution to the problem is terrifically complex, and involved an immense amount of round trip communications between the participating replicas.

It is essentially in the vein of the Liar and the Truth Teller riddle, when you know that one of the two guards you'll be speaking with will lie to you and the other will tell the truth, but not which is which:

>>> You are a prisoner in a room with two doors and two guards. One door leads to Freedom and  the other to Death – but which is which? One guard always tells the truth; the other only lies. Which is the truth-teller and which the liar? Unfortunately you do not know this either. You must choose a door, and you can ask only one single question, of only one of the guards. What (and who) do you ask to find your way to Freedom?

The solution to the riddle (an XOR) is simpler given the small number of participants. The problems gets much more complex and impractical as the number of participants grows, but with enough communication (and assuming a strict ceiling on the proportion of nodes that are fault), all honest nodes will eventually come to consensus.

In ["Practical Byzantine Fault Tolerance,"](http://pmg.csail.mit.edu/papers/osdi99.pdf) Castro and Liskov present an optimization of Lamport et al's algorithm for fault tolerant replication. It works in asynchronous environments and only adds a small amount of latency, guaranteeing in exchange that the system will be robust to arbitrary behaviors, and providing liveness and safety as long no more than `(N-1)/3` of the `N` total replicas are faulty. Similar to Paxos, Raft, and the other variants, replication happens in the context of an epoch (in the pBFT paper called "views"), in which one replica is the leader (the "primary"). The rest of the replicas are "backups", and participate passively as individuals, but can come together to form a supermajority that can elect a new leader if the current leader is deemed faulty or just too slow.

Most of the papers we've read for [class](http://triffid.cs.umd.edu/818/) this semester have assumed the non-Byzantine case, which is helpful; in a trusted environment, we can take additional shortcuts (e.g. ePaxos) and expect much lower latencies. However, though the pBFT paper was published nearly 20 years ago now, it is still a basis (or inspiration) for many distributed ledger implementations (e.g. Hyperledger, Ripple, Stellar).

