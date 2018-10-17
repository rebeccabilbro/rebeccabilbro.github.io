---
layout: post
title:  Bolt-on Availability with Salt
image:
  feature: pepper_crop.png
date:   2018-10-16 16:29
tags:   class_readings
---

A number of the papers we've read and the implementations we've been discussing so far in 818 have concerned systems that favored availability over consistency; in these papers, the discussion has been about how to achieve an acceptable amount of consistency in an AP system. The "Salt: Combining ACID and BASE in a Distributed Database" takes a different tack; in this paper, Xie et al assume a traditional transactional RDBMS as the starting point, and introduce a bolt-on approach to availability.

I appreciate that the authors take a sympathetic stance towards organizations whose applications are built atop RDBMS, only to realize later that they are victims of their own success, and that the only way to scale out and up is to reimplement everything from scratch in a more available system. Obviously, this is going to be a bitter pill to swallow. The solution that the authors propose reminded me in some ways of the "Bolt-on Causal Consistency" paper, in the sense that in the same way that it might be possible to add a consistency layer to an AP system, it may also be possible to add availability to a CP system. 

They achieve this by introducing a set of new, more finely-grained locks that can be used to interleave BASE transactions with ACID ones without compromising the atomicity of the ACID transactions. Their notion of BASE transactions are ones that are wrapped by special statements that delineate that this fine-grained locking should be used. In addition to the usual ACID locks, alkaline locks are used during active subtransactions inside a BASE transaction, and saline locks are used to help share state across BASE transactions.

Because BASE transactions expose intermediate state to every other BASE transaction, one of the limitations of BASE-ifying a lot of transactions in an existing RDBMS is that more and more state must be interleaved, which very quickly increases the complexity of the implementation. Nevertheless, Salt seems like a very clever way of enhancing availability in a CP system without having to start over from scratch!