---
layout: post
title:  Notes on Immutability
date:   2018-08-26 09:04
---

Conventional wisdom says that concurrent architectures are bound by tradeoffs between efficiency and complexity. More concurrency offers more efficiency, which comes at the cost of architectural complexity. Implementing concurrency requires more cognitive overhead. The code may be much more fragmented, making things like debugging and maintenance tough. More importantly, concurrency can also compromise consistency, because concurrent operations (e.g. near-simultaneous read and writes) can lead to data integrity issues. Consumers and developers alike have some expectation of immutability. In this post I talk through my notes on reading Pat Helland's ["Immutability Changes Everything"](http://cidrdb.org/cidr2015/Papers/CIDR15_Paper16.pdf).


## What is Concurrency?

In my post on the [Actor Model](https://rebeccabilbro.github.io/actor-model/), I briefly touched on concurrency, which means a program that has been broken down into steps that can be successfully executed independently and even out-of-order. Concurrent architectures, when implemented well, offer tremendous speed, scaling, and efficiency (e.g. time, power usage). In some cases, they may also offer security advantages (e.g. handling DDOS attacks). Concurrency can be especially useful for I/O bound tasks, or long running programs that require interaction with lots of servers or users.

## What is Immutability?

In programming discussions, immutability generally refers to objects; mutable objects are ones that can change (e.g. have their values reassigned, be appended to, etc); immutable objects can't change after they're created. In general, primitives tend to be immutable while container-like types tend to be mutable, though this isn't a hard and fast rule in every language. For instance, in Python, the primitives `int`, `float`, `str`, and `bool` are immutable, while `list`, `dict`, and `set` are all mutable. On the other hand, Python `tuples` (non-primitive) are immutable. On the other hand, in Go data structures are not immutable, except for strings.

In the context of Helland's paper though, the term *immutability* is used a bit more generally, to describe large-scale data storage. In this sense, immutability means that data inside a database does not change except to accumulate. This is convenient for distributed databases, because discrepancies between copies of the database can be easily rectified via updates, which will only ever come in the form of new writes, never re-writes or deletions. This works even better when we maintain redundant copies of the database around, just in case something goes wrong with the ones we're depending on.

> "We can now afford to keep immutable copies of lots of data, and
one payoff is reduced coordination challenges." - Pat Helland

In other words, coordination is now a lot more expensive than keeping more copies and adopting the practice of not deleting things.

##  The Truth is the Log

> " The truth is the log. The database is a cache of a subset of the log." - Pat Helland

Append-only computing describes a general approach and comprises multiple strategies, including ones that seem like they may have outlived their usefulness for a lot of modern applications (like single master computing, which has been superseded by distributed single master like Paxos).

Helland calls himself a "database old timer" in the sense that he came up thinking of relational databases as the only type of database (i.e. before the NoSQL revolution). But interestingly, Helland still frames relational databases as the source of truth (the "Data on the Inside"), casting "Data on the Outside" as secondary data products (messages, files, documents, web pages). This "outside" data is conceptualized as unlocked, immutable, uniquely identifiable, and versioned.

## DataSet vs. Database

Helland defines a "DataSet" as a snapshot or extract from a database. It's conceived as a fixed and immutable set of tables, including both schema information and metadata as well as data. It is created, consumed for reading, then deleted. They might be relational or not -- potentially as graph, a hierarchy (JSON), a set of key-value pairs, etc. Moreover, it doesn't take any management; because it is immutable, we don't have to worry about locking or controlling updates.

Databases, by contrast, are mutable (except when we're taking a snapshot of them or doing analytics, when we might freeze things).

It's clear though from Helland's writing that these two conceptualizations are somewhat outdated, not necessarily because they are not correct, but because people are using DataSets and databases in new ways (including in unsystematic, incorrect, and dangerous ways, though he doesn't say that explicitly). Based on what I have observed in my work as a data scientists, DataSets are sometimes joined with database tables, are sometimes treated as sources of truth, and are sometimes even treated as mutable!

> "By watching and monitoring the read usage of a DataSet, you may
realize new optimizations (e.g. new indices) are possible." - Pat Helland


## Vocab & Acronyms

 - [Dynamic random-access memory](https://en.wikipedia.org/wiki/Dynamic_random-access_memory) (DRAM) is a type of random access semiconductor memory that stores each bit of data in separate, small capacitors within an integrated circuit.
 - [Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write) (COW) (aka implicit sharing or shadowing) is a technique for coordinating modifications in a memory-efficient way. For example, let's say we log into a shared virtual machine and prepare to make some changes. Under COW, the kernel intercepts to create a copy or fork, but not until we actually start making changes. If we don't end up making any changes, the copy never gets made.
 - [A solid-state drive (or solid-state disk)](https://en.wikipedia.org/wiki/Solid-state_drive) (SSD) is a storage device that uses integrated circuit assemblies as memory to store data persistently.
 - [A hard disk drive (aka hard disk, hard drive, or fixed disk)](https://en.wikipedia.org/wiki/Hard_disk_drive) (HDD) is an electromechanical data storage device that stores and retrieves information using hard spinning disks coated in magnetic material.
 - [A log-structured file system](https://en.wikipedia.org/wiki/Log-structured_file_system) (LSF) is a file system in which data and metadata are written sequentially to a circular buffer called a log.
 - [A log-structured merge tree](https://en.wikipedia.org/wiki/Log-structured_merge-tree) (LSM) is a data structure that maintains data in key-value pairs, which provides indexed access to files with high insert volume (e.g. transactional log data).
 - [A database management system](https://en.wikipedia.org/wiki/Database) (DBMS) is a software application that interacts with end users, other applications, and the database itself to capture and analyze data.
 - A **"DataSet"** is a fixed and immutable set of tables, a snapshot or extract from the database. It includes both schema information and data. It is created, consumed for reading, then deleted. DataSets may be relational or represented as a graph, a hierarchy (JSON), etc. Because it is immutable, there’s no need for locking and no worries about controlling updates. It doesn't take any management.
 - A **linear version history** is **strongly consistent**. One version replaces another. There’s one parent and one child. Each version is immutable. Each version has an identity. Typically, each version is viewed as a replacement for the earlier versions.
 - A **directed acyclic graph** of version history may have many parents and/or many children. This is sometimes called **eventual consistency**.
 - Strongly consistent ([ACID](https://en.wikipedia.org/wiki/ACID_(computer_science))) transactions appear as if they run in a serial order. This is sometimes called **serializability**. ACID stands for:
    - [Atomicity](https://en.wikipedia.org/wiki/Atomicity_(database_systems)): An atomic transaction is an indivisible and irreducible series of database operations such that either all occur, or nothing occurs.
    - [Consistency](https://en.wikipedia.org/wiki/Consistency_(database_systems)): Any given database transaction must change affected data only in valid ways, i.e. according to all defined rules individually and in combination.
    - [Isolation](https://en.wikipedia.org/wiki/Isolation_(database_systems)):  Determines how transaction integrity is visible to other users and systems. Lower isolation levels increase the ability of many users to access the same data at the same time, but increase the number of concurrency effects (such as dirty reads or lost updates) users might encounter. A higher isolation level reduces the types of concurrency effects, but requires more system resources and increases the chances that one transaction will block another.
    - [Durability](https://en.wikipedia.org/wiki/Durability_(database_systems)): guarantees that transactions that have committed will survive permanently. Durability can be achieved by committing log records to non-volatile storage before considering the transaction complete. In distributed transactions, all servers must coordinate before a commit can be acknowledged. This is usually done by a two-phase commit protocol.
 - [Google File System](https://en.wikipedia.org/wiki/Google_File_System) (GFS) is a proprietary distributed file system developed by Google to provide efficient, reliable access to data using large clusters of commodity hardware.
 - [Hadoop Distributed File System](https://en.wikipedia.org/wiki/Apache_Hadoop) (HDFS) is a distributed file-system that stores data on commodity machines, providing very high aggregate bandwidth across the cluster.
- A [Globally Unique Identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier) is a 128-bit number used to identify information in computer systems.
- A [Service Level Agreement](https://en.wikipedia.org/wiki/Service-level_agreement) is a commitment between a service provider and a client regarding things like quality, availability, and responsibilities.
- **Wear leveling** is a form of copy-on-write and treats each version
of an SSD block as an immutable version.
- **Shingled Disk Systems** aim to increase storage density and overall per-drive storage capacity via [shingled magnetic recording](https://en.wikipedia.org/wiki/Shingled_magnetic_recording).

## Further Reading

 - [Bernstein, P.; Hadzilacos, V.; Goodman, N. (1987).
"Concurrency Control and Recovery in Database Systems",
Addison Wesley, ISBN 0-201-10715-5.](https://www.researchgate.net/publication/31637827_Concurrency_Control_and_Recovery_in_Database_Systems_PA_Bernstein_et_al)
- [Dean, J.; Ghemawat, S. (2004). "MapReduce; Simplified
Data Processing on Large Clusters". OSDI ’04: 6th
Symposium on Operating System Design & Implementation.](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf)
- [DeCandia, G.; Hastorun, D.; Jampani, M.; Kakulapati, G.
Lakshman, A.; Pilchin, A.; Sivasubramanian, S.; Vosshall, P.
Vogels, W. (2007). "Dynamo: Amazon’s Highly Available
Key-Value Store". Proc of the 21st ACM Symp on Operating
Systems Principles.](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Ghemawat, S.; Gobioff, H.; Leung, S. (2003) "The Google
File System". Proceeedings of the 19th ACM Symposium on
Operating Systems Principles – SOSP ‘03](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)
- [Gibson, G.; Ganger, G. (2011) "Principles of Operation for
Shingled Disk Devices". Carnegie Mellon University
Parallel Data Lab Technical Report CMU-PDL-11-107.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.206.3824&rep=rep1&type=pdf)
- [Helland, P. (2005) "Data on the Outside versus Data on the
Inside" Proceedings of the 2005 CIDR Conference
(Conference on Innovative Database Research).](http://cidrdb.org/cidr2005/papers/P12.pdf)
- [Helland, P. (2014) "Heisenberg Was on the Write Track".
Abstract: Proceedings of the 2015 CIDR Conference
(Conference on Innovative Database Research).](https://pdfs.semanticscholar.org/edbd/0aa0a6aece5ded955a6b6cf96c5e023ac899.pdf)
- [Isard, M.; Budiu, M.; Yu, Y.; Birrell, A.; Fetterly, D. (2007)
"Dryad: Distributed Data-Parallel Programs from Sequential
Building Blocks" European Conf on Computer Systems
(EuroSys).](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/03/eurosys07.pdf)
- [Karger, D.; Lehman, E.; Leighton, T.; Panigraphy, R.;
Levine, M.; Lewin, D. (1997). "Consistent Hashing and
Random Trees: Distributed Caching Protocols for Relieving
Hot Spots on the World Wide Web". Proc. of the 29th
Annual ACM Symp on Theory of Computing.](https://www.akamai.com/es/es/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf)
- [Lamport, L. (1998). "The Part-Time Parliament",
ACM Transactions on Computer Systems (TOCS), Volume
16, Issue 2, May 1998.](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)
- [McKusick, M.; Quinlan, S.; "GFS: Evolution on Fast
Forward" (2009) ACM Queue, August 7, 2009.](https://queue.acm.org/detail.cfm?id=1594206)
- [O’Neil, P; Cheng, E.; Gawlick, D.; O’Neil, E. (1996) "The
Log-Structured Merge-Tree (LSM-tree)". Acta Informatica 33 (4).](https://www.cs.umb.edu/~poneil/lsmtree.pdf)
- [Rosenblum, M.; Ousterhout, J. (1992) "The Design and
Implementation of a Log-Structured File System". ACM
Transactions on Computer Systems, Vol. 10, Issue 1.](https://people.eecs.berkeley.edu/~brewer/cs262/LFS.pdf)
