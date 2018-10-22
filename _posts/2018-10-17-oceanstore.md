---
layout: post
title:  Global Data Storage and Distributed Hashing 
image:
  feature: pepper_crop.png
date:   2018-10-21 17:41
tags:   class_readings
---

In the late nineties and early 2000's, the question of how best to support decentralized filesystems became a very hot and relevant topic. From Napster to Gnutella to Limewire and Kazaa, it suddenly became clear that data storage was a problem of social network behaviors just as much as it was one of hardware efficiencies. In the [Chord](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf) and [OceanStore](http://www.srhea.net/papers/asplos00.pdf) papers, we get some insight into academia's algorithmic responses to the p2p revolution.

## Chord

Suppose we have a peer-to-peer network with lots of files stored throughout. This is essentially a decentralized file system; so how should we go about enabling the system to communicate across its many nodes? At the most basic level, from any given node in the system, we need to be able to find where a certain file is stored. 

A naive solution would be to give every node a map of every other node in the system. Although it would give a direct mapping, this would be a difficult map to maintain as nodes enter and exit the system. What we need is a way to do this without have to create or maintain a centralized mapping of all the nodes in the system.

Another option would be to give each node a map to a few friend nodes, each of which are mapped to a few other friends. While depending on how we implement the friend-mapping, this might not be very efficient. The solution presented by [Chord](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf) is method for making those mappings in a way that is decentralized, scalable, dynamic, and fast.

Inside the Chord identification space, new incoming keys are assigned to a buddy node with the same identifier or the one just higher. The key's buddy is called it's "successor node". As new nodes join the network, they inherit some of the key-buddies of their successors, and as nodes leave the network, they delegate their key-buddies to their successors. In order to work correctly, Chord nodes only need to know their successors. However, in order to make searching more efficient, nodes also maintain a map ("finger table") to a few other nodes. which effectively serves as a phone-tree. That means nodes can leverage their successors to look for close nodes, and leverage their finger tables to look for more distant nodes. This aids with the scaling of the system because "The finger pointers at repeatedly doubling distances around the circle cause each iteration of the loop in `find_predecessor` to halve the distance to the target identifier."

One of the potential weaknesses of Chord is that it might be fragile to partitions and Byzantine behavior, and also that it doesn't leverage network locality, which might help with speed over long (physical) distances. Nevertheless, Chord offers a very powerful protocol for creating and maintaining distributed hash tables in a fully decentralized way.

## OceanStore

In one sense, the major contribution of the [OceanStore](http://www.srhea.net/papers/asplos00.pdf) paper is the notion that data storage could have very nearly become another regular utility alongside now-familiar companions like our electricity, gas, telephone, television, and internet connections. 

The paper is clearly inspired by some of the work we've already read in class, taking cues from the Bayou system to inform the strategy for disseminating updates via pairwise anti-entropy sessions in the secondary tier, and leveraging the Elephant system's temperature-based version-retirement approach for archival (and also somewhat foreshadowing later deep archival strategies such as the Read-Solomon erasure codes used in FaceBook's f4 system).

From an algorithmic perspective, the primary contributions of the paper are it's adaptation of (1) the randomized hierarchical distributed data structure introduced in Plaxton et al's "Accessing nearby copies of replicated objects" and (2) attenuated Bloom filters for expedient routing.

The distributed data structure used for routing in OceanStore uses hashing to uniquely identify content (e.g. pictures, songs, documents) independently of its location. Every resulting object gets a tree that points to the server where the actual data is stored. Nodes in the network can not only make requests (e.g. look for content) and serve requests, they can also route requests from nodes to other nodes efficiently (using suffix routing) to the nearest copy of the desired file.

OceanStore uses attenuated Bloom filters to help figure out where to look for files. Nodes store both regular and arrayed Bloom filters, which point to data in the node's immediate vicinity, and in it's more distant network, respectively (for instance, a node `n`'s attenuated filter of level `x` indicates files that are available via nodes that are `x` hops away from `n`).

In the wake of the p2p revolution, something like OceanStore was a plausible eventuality (which is why the authors are so focused on trust and counteracting Byzantine behavior), and though it has not played out as imagined by the authors, the paper is nevertheless a valuable contribution insofar as it illustrates how the requirements of such a decentralized, networked data storage system could be achieved.
