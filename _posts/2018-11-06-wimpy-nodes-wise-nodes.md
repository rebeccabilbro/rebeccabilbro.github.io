---
layout: post
title:  Wimpy Nodes, Wise Nodes
image:
  feature: pepper_crop.png
date:   2018-11-06 18:35
tags:   class_readings
---


In a distributed storage system, one big question is how much state should be stored on any given node. Decentralized systems tend to give nodes a lot more state, so that they have enough information about the system as a whole to make more independent decisions. However, requiring nodes to maintain a large amount of state can cause problems and also be slow, which is why many distributed systems opt for architectures with strong leaders. In ["Scalable Consistency in Scatter"](https://homes.cs.washington.edu/~tom/pubs/scatter.pdf) and ["FAWN: A Fast Array of Wimpy Nodes,"](http://www.sigops.org/s/conferences/sosp/2009/papers/andersen-sosp09.pdf) we see examples of papers that attempt to balance between decentralization and speed.

## Scatter

Part of the novelty of Scatter (particularly given that it came out in 2011) is that it borrows ideas from two fields; the consistency community (e.g. synchronous replication w/ consensus), and the p2p community (e.g. the DHT-type papers we explored in Chord, Sinfonia, OceanStore, etc). 

Scatter is essentially a DHT that is optimized for systems with potentially a *lot* of churn (i.e. along the lines of what the OceanStore folks had in mind). The other DHTs we looked at were really good at scaling, but not so good with things like churn, system heterogeneity, and faults. Faults are bad for DHTs because of the protocols they use for adding and removing nodes, which aren't atomic. For instance, when a new node is added to something like Chord, we have to update the state of the predecessor and the successor nodes; if something goes wrong in the middle of those updates, we could easily get an anomaly. Or what if two nodes were added concurrently?! This is not going to be a big pain point in a stable, homogeneous system, but that's not often what we have in practice.

Scatter's solution is to adapt DHT so that the nodes are in fault-tolerant `groups`, within which state (e.g. memory nodes, keys, leaders) is replicated using Paxos, and across which state is communicated using distributed transaction protocols. This combination allows Scatter to provide consistent routing and namespace partitioning within high-churn networks.

One question I had about Scatter was about how to address a situation where the majority of nodes in a group fail at almost the same time, interrupting the reconfiguration process (I mean, if we're considering high-churn, this does seem like a plausible scenario). I suppose we could make the groups larger, so they'd be more resilient, but that would also make them slower, since they're all required to agree in order to replicate. Perhaps something like ePaxos would help?

## Fawn

The FAWN paper is a bit strange, in that it is attempting to make both a scientific and an economic argument; first that flash-based distributed computing is better because it's faster, and also that it's better because it's more energy efficient. To me the two arguments get a bit muddled together in the paper. 

I think, however that the main argument is the one about energy efficiency, which aims to show that a large network of tiny flash microprocessors (`wimpy nodes`) can shoulder the load of a large data-intensive application just as effectively as an expensive cluster of heavy-duty disk-based nodes, at much lower cost. To prove out this hypothesis, the authors built a log-structured (similar to GFS) key-value store on top of the FAWN architecture and tested not only it's speed and energy usage, but also its availability and consistency. 

What I liked most about this paper were the discussions of the system requirements under which specific deployments of FAWN would be most effective; first, for large overall data storage requirements, FAWN nodes using disks would be most cost effective; for small datasets accessed frequently, FAWN nodes using DRAM would give a better bang for the buck; the best overall compromise is FAWN nodes on SSDs. This kind of per-use-case cost reasoning seems like it should have led to an advent of more specialized commercial options for distributed storage the way we have for distributed computing, where you can make good decisions about how big an EC2 instance you need, or how long your Spark cluster needs to run, or whether you can run your function inside a lambda instance, etc.

I also noted that the primary author of this paper is David Andersen, who was (I believe) Iulian Moraru's advisor -- I suppose this work must have been something he was doing before he and Iulian decided to go down the ePaxos research path?