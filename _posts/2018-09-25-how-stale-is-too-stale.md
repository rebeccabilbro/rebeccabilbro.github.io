---
layout: post
title:  How Stale is too Stale?
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-25 13:08
---

Proposed around 1999, the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) taught us that it was unreasonable to expect a distributed system to guarantee simultaneous consistency, availability, and partition tolerance. So, throughout the 2000's, as distributed systems became more common in commercial contexts, and also as systems became increasingly distributed, companies made hard choices. Oftentimes, this involved trading off the promise of "the illusion of a single copy" (strong consistency) for increased availability. In "Quantifying Eventual Consistency with PBS," the authors present an actual set of metrics that can be used to compare two eventually consistent systems, or to compare a single weakly consistent system with different parameters. In this post, I'll discuss my take on their [paper](http://www.bailis.org/papers/pbs-vldbj2014.pdf).


## Fresh Enough

I found the "Quantifying Eventual Consistency" paper particularly interesting because from the very beginning, it seems to acknowledge that consistency is a spectrum, and that we should "treat consistency as a continuous quantitative metric". The readings we have done thus far for class have represented consistency as either a black-and-white thing (e.g. guaranteed or not), or as a qualitative, squishy thing (e.g. "weak consistency", "eventual consistency"). Yet, as Bailis et al. explain, "faced with a requirement for high availability and low latency, many production data stores have turned to weaker semantics to provide availability in the face of network patterns." Neither the perspective of consistency as a boolean or as a qualitative measure is particularly useful when it comes to bargain shopping for the best distributed database tools for your use case. Good heuristics are sometimes more valuable than guarantees.


## Quorums

This is also the first paper we've read that discussed quorums, though they didn't go into a great deal of depth on implementation. It's clear that the quorum architecture offers some of the flexibility of the gossip protocol we saw in Bayou, with more clear structure and governance, which seems to make for a more performant system. The paper also touches briefly on the differences between strict quorums (which ensure that read and write replica sets overlap, as in a majority quorum) and partial quorums (in which at least two quorums in the system do not overlap). The authors mention that Dynamo, Cassandra, Voldemort, and Riak (all AP-type NoSQL systems that offer key-value storage) all use the same approach to replication, which they refer to as "expanding partial quorum systems." So, if we want to keep data fresh enough for our application, which should we pick? Conveniently, the authors offer up a metric that allows us to actually quantify the tradeoff between latency and staleness. Even better, they use the metric to compare tradeoff in two systems in a production context (LinkedIn and Yammer)!


## Experimental Results

The experimental results in the paper were very interesting, as the authors were able to actually quantify things like the extent to which extra slow writes and extra fast reads result in staleness. From the perspective of a company trying to make a decision between strong consistency (and potential latency problems) and weak consistency (with potential staleness issues), we can see how these kind of metrics move the discussion away from guesswork and buzzwords into the realm of objective measures. From the perspective of LinkedIn and Yammer, it's immediately clear how useful the staleness probability metric would be in experimenting with new hardware configurations (e.g. using SSDs to reduce write variance) or with adopting new techniques (e.g. more explicit memory management, asynchronous flush writes) to improve consistency.


## Questions

One of the questions I have is about whether there are newer data stores that use different replication protocols from those employed in Dynamo and the others mentioned in this paper (the authors suggest there at least weren't any in 2014)? I'm also curious about how the partial quorums described in this paper work in concert with anti-entropy techniques (like those described in the Bayou paper). Finally, I believe this paper came out around the same time as Raft, so it would be interesting to hear how that impacted discussions around consistency.
