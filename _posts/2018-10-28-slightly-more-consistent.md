---
layout: post
title:  Slightly More Consistent 
image:
  feature: pepper_crop.png
date:   2018-10-28 15:15
tags:   class_readings
---

Over the last few weeks, we've spent a lot of time with eventual consistency. Therefore it's useful to revisit causal consistency, which while still a "weak" consistency model, is stronger than eventual because everyone within the system agrees on the order of operations that are causally-related. However, causal consistency *does not* impose order on concurrent operations.

Any two unrelated, concurrent operations PUT(val(x)) to key(y) and PUT(val(r)) to key(q) can be written in any order. Replica A might put val(x) to key(y) before putting val(r) to key(q), while replica B puts val(r) to key(q) first. This means that two replicas may diverge permanently, but that's okay under regular causal consistency, even in cases where the concurrent operations are both puts to the same key. The expectation is that the conflict will be dealt with at the replica level, perhaps via the application layer.

## COPS

Causal+ consistency, described in the [COPS paper](https://www.cs.cmu.edu/~dga/papers/cops-sosp2011.pdf) seeks a greater level of consistency than this. Within clusters, COPS uses logical clocks to timestamp each operation, to produce a single global ordering of all the puts and gets to a given key. Conflicts are addressed using the latest-writer-wins strategy (though they say that this could also be dealt with at the application level, which is like what we saw in the [Bolt-on paper](http://www.bailis.org/papers/bolton-sigmod2013.pdf), published a couple years after this one). 

There are some interesting strategies here, like using a monotonically increasing function to ensure that after a certain value has been returned for a given key, no older version of that key can ever be returned in the future. They call this the "progressing property".

Local COPS clusters are strongly consistent because we can assume that latency will be pretty low and that there won't be partitions. Across clusters L and M, COPS uses dependency tracking (which looks similar to the "causal cuts" that appeared in Bolt-on), so in addition to cluster M requesting updates to all the keys in cluster L, M also retrieves the list of dependencies for each of those keys; this allows cluster M to double check that it's versions of the dependencies for all the keys are up-to-date with L's before proceeding with the updates. 

## Ambry 

In Bailis et al's "Quantifying Eventual Consistency", we were given probabilistically-bounded staleness, a way to quantify how stale an eventually consistent system was at any given time. One of the production systems Bailis et al looked into and benchmarked was Linkedin's. At the time, Linkedin was using [Voldemort](https://www.project-voldemort.com/voldemort/), a distributed key-value storage system, which apparently turned out to be a bit *too* eventual as Linkedin grew in size and popularity.

In the [Ambry](http://dprg.cs.uiuc.edu/docs/SIGMOD2016-a/ambry.pdf) paper, we start to get more of a sense of where Linkedin's previous system was underperforming. For one thing, they were dealing with large blobs similar to those described in Facebook's [f4](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf) paper, but with the added problem of heterogeneity; they don't just have large blobs like videos and pictures, they also have documents, slides, and other unstructured text files. This calls to mind a bit the struggles discussed in the [GFS](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf) paper, which also had to grapple with the storage of files of dramatically varying sizes. The other big problem Linkedin had was rebalancing load across nodes as clusters grew. Their solution was to map blobs to virtual units (somewhat similar to f4's logical nodes) called "partitions", and to treat these "partitions" a bit like the log-segments introduced in the [LFS paper](https://web.stanford.edu/~ouster/cgi-bin/papers/lfs.pdf), which can be efficiently written to sequentially. Large, uniform partition sizes help to ensure that temperature is balanced effectively across partitions (though as of the time that they published this paper, it sounds like they hadn't yet gotten around to implementing a temperature-based deep archival system with erasure coding). "Partition pools" enable already-written-to-disk partitions to be redistributed across nodes as clusters grow (or shrink, theoretically, though Linkedin doesn't have too much competition so they don't seem too worried about that).

Together, these techniques give Linkedin more horizontal scalability in Ambry without sacrificing availability.


