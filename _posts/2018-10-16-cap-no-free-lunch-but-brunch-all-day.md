---
layout: post
title:  No Free Lunch, but Brunch All Day
image:
  feature: pepper_crop.png
date:   2018-10-16 15:16
tags:   class_readings
---

While the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) was a significant insight into the tradeoffs in distributed systems, it also led to a lot of confused expectations and cop-outs. At a high level, the CAP theorem states that a distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance. As a result, many came to believe that they would have to choose either available, partition-tolerant tools (like NoSQL DBs) or consistent, partition-tolerant tools (like NewSQL DBs). Unfortunately, this turns out to be a bit of a false choice, since there is a significant amount of nuance to availability and consistency beyond black-and-white guarantees. In Bailis et al's "Highly Available Transactions: Virtues and Limitations," we get the chance to dig a bit deeper into specific features and signatures of consistency and availability that can be implemented, as well as a clear delineation of the ones that are (and are not) mutually exclusive.

For instance, availability can mean different things depending on whether the distributed system allows for "stickiness" (e.g. allowing clients to stick to servers that can in turn cache reads and writes -- this was a feature we saw in the Facebook papers), and depending on the nature of the transactions. With sticky availability, we're guaranteed a response for every execution; assuming we have that, sticky transactional availability ensures we either always commit or else internally abort. For replica availability, we're guaranteed to get a replica for every data item we want to read or write to, and assuming we have that, transactional availability ensures we either always commit or else internally abort.

## Transactional Semantics and Isolation Levels

I appreciated that the authors frame the discussion in terms of transactional semantics and specific isolation levels. These are not only easier for me to reason about, they also enable a pretty clear-cut set of definitions that can be used to specify tradeoffs very precisely. Namely, HAT can guarantee: no dirty writes, no dirty reads, item cut isolation, predicate cut isolation, monotonic atomic views, monotonic reads and writes, Lamport's "happens-before" relation, and eventual consistency. If the HAT is sticky available, we can also guarantee read your writes, the illusion of serialization, and causal consistency.

On the other hand, HAT *cannot* guarantee the prevention of lost updates or write skew (cycles), linearizability, strong serializability, or F>1 fault tolerance.

## Chicken and Egg

There is perhaps one downside of couching the conversation about what is "good enough" in context of existing applications' satisfactory compromises between availability and consistency. The authors write, "...our inability to provide serializability in arbitrary HATs appears non-fatal for practical applications." One interpretation of this (and the one that the authors seem to be implying) is that the absence of serializability guarantees isn't a real hinderance to practical applications. However, another way to interpret this is that the only kinds of applications that are currently *practical* are the ones that can get by without serializability guarantees.

Much like Bailis' earlier probabilistically-bounded staleness paper, what I like about this paper is that it takes a very practical approach to examining the specific, precise tradeoffs between different features of distributed systems. As such, it not only clarifies what specifically it is unreasonable to expect inside a single distributed system, but also about the combinations of features we *should* be able to expect as consumers. There may be no free lunch, but there's brunch all day.