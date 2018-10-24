---
layout: post
title:  Sinfonia and Dynamo 
image:
  feature: pepper_crop.png
date:   2018-10-23 17:33
tags:   class_readings
---

An exploration of alternative approaches to building distributed systems, including Sinfonia's object-oriented approach, and Dynamo's highly available key-value store.

## Sinfonia

From an object-oriented programming perspective, I found Sinfonia's strict interface rather reassuring. They have imagined a kind of distributed system where the central object is not a replica or a chunk of memory, but an abstract (mini)transaction.  

This allows for a strong contract between the application layer and the system about how transactions will take place and be structured (as comparisons, reads, writes, and execute-and-commits). My understanding is that these different methods defined on the minitransaction object have specified positional arguments that indicate things like memory address, offset, and byte content.

This also means that certain methods are compatible and can be grouped together (somewhat reminiscent of the commit grouping strategy in the Elephant filesystem), such as non-conflicting writes; in Sinfonia they call this grouping "piggybacking." Piggybacking then allows for the execute-and-commit method to be a single operation, saving a round trip of communication.

Some of the other things that stood out to me about Sinfonia is that while there are leaders (called "coordinators" here). they're more akin to public servants, since they don't vote and they don't have logs. That means that Sinfonia blocks when *participant* nodes crash, but not when coordinators crash. Periodically, a maintenance coordinator scans for crashed coordinators and executes a repair communication sequence with the participants. Participants that attempt and fail to get all the locks they need for a complete operation send an abort message to their coordinator and release any locks they hold (this helps avoid deadlocks).

I think one of the most interesting observations from the experimental results was the poor scaling as minitransactions tried to interact with a greater percentage of the overall nodes in the system. The lesson learned is that each minitransaction should involve as few memory nodes as possible ("Across minitransactions, spread load; within a minitransaction, focus load"). 


## Dynamo

There's something a bit bracing in the notion of a distributed system built not on principles of elegant design or mathematical correctness, but on the adage that the customer is always right.

Amazon's answer to the NoSQL revolution, Dynamo, was predicated on some pretty substantial (manual) introspection of their legacy RDBMS, and the subsequent realization that the majority of the queries happening under the hood were just returning a single row (e.g. the name, price, color, size, and manufacturer of product X). Likewise, most of the writes were also pretty precise, modifying only a single table. In other words, there weren't a lot of joins going on, which is basically the whole point of normalization.

The main insight of the Dynamo paper is that user experience is more important than the truth. Interestingly, we saw something quite similar in the Bayou paper, which also privileged UX and went so far as to make conflict part of the UX of the apps they built on top of their system ("Oh, I'm sorry that room isn't available at 10AM, but it is at 10:30AM, how does that work for you?"). Dynamo takes a different approach, which is essentially a read-now-and-apologize-later strategy ("push the complexity of conflict resolution to the reads in order to ensure that writes are never rejected"). The worst case for Amazon is that they end up accidentally selling more X than they have, in which case they can just source more X.

This calls for creating a kind of hierarchy of apps-on-top-of-apps to ensure customers have a seamless and enjoyable buying experience. This is achieved by treating all modifications to the key-value store as new versions that are timestamped using a vector clock, and can be sorted out at the internal application layer that knows how to deal with things like merges of inconsistent shopping carts.

As someone who has used Dynamo extensively at work, this is the first time it's occurred to me that, useful as it is, it really isn't optimized for anyone operating at a scale smaller that Amazon's. Similar to the GFS papers we read earlier in the semester, it's clear that the advantages for "big players" go far beyond just the economies of scale, extending to complex internal optimizations and system-to-application contracts that may not always generalize to the average use case.