---
layout: post
title:  Replication and Consistency for Social Media
image:
  feature: pepper_crop.png
date:   2018-10-14 12:10
tags:   class_readings
---

Replication and consistency needs are not uniform across all contexts; some applications we've read about are extremely write-intensive, such as GFS, which must enable users to modify files many times over while also supporting the freshest reads possible. Others, however, significantly constrain the actions users can take, effectively opening up unique opportunities for the implementation of highly specialized distributed systems. This is the case with Facebook's f4, a distributed storage system designed to more efficiently house social media data as it ages.

## How Volumes are Made 

As discussed in "F4: Facebook' Warm BLOB Storage System," blobs are the basic building block in Haystack, which is Facebook's legacy data storage system; they are "created once, read many times, never modified, and sometimes deleted." These blobs are aggregated into volumes, which contain files along with their metadata, an index that maps out where all the storage machines are in the system, and a "journal" file that keeps a record of any deleted files (note that the f4 paper does not seem to go into detail about how concurrency is achieved between all the variations of the journal files that go into different volumes). One of the strategies that Facebook uses is to group blobs into heterogenous chunks of files that balance hot content (likely to be reviewed very frequently) and warm content (less likely to be viewed); this is similar to the technique we observed in the Elephant filesystem paper (where the change velocity of a file was described in terms of "temperature," and used to inform the forget protocol).

## Moving from Haystack to f4

There was a lot of discussion about how to operationally define "warm" and "hot", both in terms of how long it takes before reads of a piece of social media content trail off, and what type of content it is. It occurred to me that it might not be too difficult to further disaggregate content into quick- and slow-cooling categories by actually using the content data itself; presumably patterns would emerge such as photos of scenery cool faster than photos of faces. 

I did not get a very clear sense about the details of the strategy for moving content from Haystack to f4, but my understanding is that the migration work was essentially on a timer. The first three months everything is on Haystack; after that things start to get migrated to f4, but it wasn't very clear from the paper what the algorithm was to determine when to move a specific volume from Haystack to f4. They did explain that for a period after the migration, the volume is available on both Haystack and f4.

The authors reason that most of the deletes will happen when blobs are hot, so much of the heavy lifting of deletion and garbage collection is dealt with by Haystack. In Haystack, the controller tier periodically does compaction and garbage collection to find volumes that contain a lot of files that have been deleted and reclaim space. By contrast, when things are deleted after they've been moved to f4, really only their keys are deleted. 

## So Many Copies

The thing that really struck me about the f4 paper is the extreme degree of replication; across datacenters, servers, stacks, etc. The f4's buddy blocks were particularly interesting, providing erasure coding (which I don't know very much about but understand has to do with bit-level redundancy) via the Reed-Solomon encoding technique. That's a lot of copies, which seems rather expensive for a free application...

## Weak but not *that* Weak Consistency

The "Existential Consistency" paper describes the Facebook team's development of a new real-time consistency health check measure. In production, this metric is designed to quantify just how weak Facebook's weakly consistent system is at any given moment. 

One of the first things that caught my attention is the authors' claim that there was no other means of quantifying eventual consistency to date for a large social media application -- yet as I recall, Bailis' "Quantifying Eventual Consistency" paper did just that for LinkedIn (much later in the paper they say they were inspired by Bailis' work on probabilistically-bounded staleness). Their phi-consistency measure does seem unique, however, in so far as it is possible to compute it in real time and therefore using it in realtime monitoring.

Another thing that occurred to me while reading this paper is that this is the first time we have formally encountered sharding. Presumably the fact that Facebook uses sharding (which doesn't come with the same fault-tolerance guarantees) is the reason for all the extra copying described in the f4 paper. I think it would help to have a more explicit conversation about the impact of sharding on guarantees and expectations for consistency, fault-tolerance, and availability.

Although it is framed as a paper "quantifying the benefits of stronger consistency," it almost seems to make the inverse economic argument, that the costs of other-than-strong consistency are neglible in the case of Facebook; in their experiments (which were naturally somewhat constrained since they're working on a production database), they found that inconsistencies, mostly stale reads, only happened about 0.0004% of the time. By their estimations, stronger consistency models would only eliminate a very small of these anomalies (many of which the authors go on to attribute to human error). 
