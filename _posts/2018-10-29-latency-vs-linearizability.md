---
layout: post
title:  Latency vs. Linearizability
image:
  feature: pepper_crop.png
date:   2018-10-29 21:58
tags:   class_readings
---

For this week in our distributed systems class, we read the Spanner and RIFL papers. Again, it feels like we're ocillating between two types of papers; the theory papers that prove correctness and then quibble over latency numbers using synthetic datasets, and industry papers that demonstrate peformance under real, significant load, but can't prove much of anything. In this post, we'll explore both RIFL and Spanner in a bit more depth.

## RIFL

Where the [causal consistency paper](http://www.bailis.org/papers/bolton-sigmod2013.pdf) proposed bolt on consistency, the [RIFL paper](https://web.stanford.edu/~ouster/cgi-bin/papers/rifl.pdf) suggests bolt-on linearizability. Linearizability is the strongest of the consistency guarantees, which is why we should be a little skeptical about the second part of the title "Implementing Linearizability at Large Scale *and Low Latency*". This semester we have swung back and forth between two types of papers; on the one hand, the theory papers that can prove correctness but quibble over latency/throughput numbers using synthetic datasets, and on the other hand, the industry papers that demonstrate performance under real, significant load, but can't prove much of anything. RIFL is in the first camp.

RIFL leverages RAMCloud, which we will read about in a few weeks, but that I gather is unique in that, by default, it holds a lot of data cached in RAM and that it has a log-structured replication scheme, which is what allows RIFL to "associate linearizability metadata with objects in the underlying store and migrate metadata with the corresponding objects."

For my part, I think the most interesting part of the RIFL paper is the use of RPCs (their RPC wrapper sounds a bit like protobufs); essentially, we see that linearizability *requires* something like an RPC, since we need both the request and the response. RIFL goes a step further and gives every RPC a UIN composed of client ID and sequence number, which can be used for a number of things, such as deduplicating RPCs, saving their results, marking them complete or not, garbage collection, and moving records around across servers.

The argument is that the write latencies, lease renewals, and garbage collection that are necessary to make RIFL function pose "neglible impact" on the overall system; however, the authors ultimately acknowledge that faulty servers might require that RIFL be implemented at multiple layers of the system, which while maintaining linearizability, will result in compounded latency costs.

## Spanner

Spanner is Google's relational-ish, schema-ish, SQl-ish globally distributed database. It offers a strong degree of availability by using sharding across continents, and within continents, across datacenters. It also offers very strong consistency guarantees. But how?

To establish consensus under geographic replication, Spanner uses Paxos (though technically any of the consensus algorithms we've studied would work). Every transaction is assigned a timestamp, which Spanner frames in terms of "global wall-clock time". This kind of timestamp allows for something the authors refer to as "external consistency", which implies a commit order in which all transactions appear to have been executed in the order in which they are observed by everyday users like me and you.

Given what we've learned about consistency and concurrency so far this semester, we should be skeptical about how such availability, consistency, and fault-tolerance can be achieved within a single system. The answer is TrueTime, a proprietary timing mechanism that sees time not as a fixed point but as an interval, and as such can account for clock skew, which is frankly unavoidable when dealing with machines that are physically so far apart. TrueTime allows Spanner to ensure that timestamp order is the same as commit order, which is the same as the order in which any two users observe the result of writes to the system. Strict 2-phase locking ensures that there is a wait between the end of an otherwise somewhat ambiguously-bounded operation and the start of another, until there is no longer any uncertainty in the temporal ordering of the two operations.

TrueTime requires atomic clocks. Atomic clocks use changes in electron energy levels to keep time, and are the most accurate way to keep time, particularly across wide areas. They also aren't cheap. If you're Google, this is a good solution. If you're smaller than Google, this solution might not be viable.