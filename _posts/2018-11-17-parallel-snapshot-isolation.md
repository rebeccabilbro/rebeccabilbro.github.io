---
layout: post
title:  Parallel Snapshot Isolation
image:
  feature: pepper_crop.png
date:   2018-11-17 13:32
tags:   class_readings
---

In ["Transactional storage for geo-replicated systems,"](http://www.news.cs.nyu.edu/~jinyang/pub/walter-sosp11.pdf) Sovran et al present a key-value store designed specifically for applications that require data replication across distant sites. Their solution, Walter, is novel in that it combines the benefits of key-value storage (e.g. the high availability that we've seen in Dynamo and Cassandra) with the safety and sanity of ACID transactions. This is an attractive combination from the perspective of the applications developer, who would rather not have to attempt to manually implement all of those guarantees at the application layer.

The implementation relies on a extension (relaxation, technically) of snapshot isolation:

>>> snapshot isolation is a guarantee that all reads made in a transaction will see a consistent snapshot of the database, and the transaction itself will successfully commit only if no updates it has made conflict with any concurrent updates made since that snapshot. [wikipedia](https://en.wikipedia.org/wiki/Snapshot_isolation)

Parallel snapshot isolation extends snapshot isolation by allowing different sites to have different commit orderings. PSI implements three properties:
- all operations read the most recent committed version at the site of a transaction as of the time it began
- write sets of "somewhere-concurrent" transactions (e.g. concurrent from the perspective of either transaction site) are disjoint.
- transactions begun and committed at a single site must subsequently exhibit the same commit order at all other sites.

PSI provides causal ordering, allowing for asynchronous replication of transactions. The reasoning is that transactions that happen within a single site will still be guaranteed by snapshot isolation. Moreover, across sites there are unlikely to be any application features that depend upon a global system ordering of all actions. The applications here are imagined to be social networking sites like FaceBook or Twitter, and in fact the authors implemented versions of both of these applications (WaltSocial and ReTwis) to prove out Walter's efficacy.

Objects are assigned to `preferred sites`, which leverage locality to enable more efficient writes (since no other sites will have to be checked for write conflicts), but the system still allows objects to be modified from any site (just more slowly if it isn't the preferred site). If an object is going to be modified frequently from many sites, `counting sets` or `csets` are used to compile commutative operations on the object (via increment and decrement), which allow for negative counts and can thus be executed in any order. 