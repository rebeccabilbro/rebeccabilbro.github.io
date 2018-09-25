---
layout: post
title:  Nuts and Bolts Consistency
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-25 19:09
---

In ["Bolt-on Causal Consistency,"](http://www.bailis.org/papers/bolton-sigmod2013.pdf) Bailis et al. show that it's possible to upgrade the consistency guarantees of existing eventually consistent data stores by implementing a "shim" layer between the database and the user-facing application. Instead of interacting directly with the database, the application interacts with the shim, and the shim talks to the database on their behalf, restricting reads and writes to ensure causal consistency.

## Conversational Artifacts

The idea of causal consistency comes from the "happened before" relation introduced in Leslie Lamport's 1978 "Time, Clocks, and the Ordering Events in a Distributed System." "Happened before" expresses a partial ordering of events in a distributed system, and can be extended to provide a consistent total ordering. Everyone seems to agree that this is the right way to order events, but it turns out to be really hard to build causally consistent systems. So instead, we build eventually consistent ones, and end up sacrificing the safety of knowing how long convergence will take.

One of the main insights of this paper is that many modern applications already have causality. Apps like Facebook, Twitter, and Reddit facilitate conversation and produce artifacts of those conversations that explicitly track causality. When you reply to someone's post, the application captures the explicit causal relationship between your reply and their original post as metadata. If only we could figure out how to put that metadata from the application into the data store...

## A Fancy Buffer

Enter the bolt-on "shim". Instead of interacting directly with the database, the application interacts with the shim (via `get(key)` and `(put(key, value, after))`, where `after` is a previous write or `None`), and the shim talks to the database on their behalf (via `get(key)` and `(put(key, value))`). In the example of the response to a post, the post is a dependency of the reply; so the reply shouldn't get `put` until the post is `put`. In other words, the metadata from the apps doesn't actually go directly into the database, but it gets used to "restrict the space of system executions," and make sure reads and writes are well-ordered. This is a neat solution that enables "a clean separation of concerns" as the authors explain, which means that they can basically implement causal consistency with out-of-the-box Cassandra and 2k lines of custom Java code.

## But How?

The problem is that it's tough to actually implement this using existing time-measuring tools. Vector clocks won't allow us to differentiate between commits that haven't yet been seen and those that have been overwritten; pointers between can be overwritten. The solution is "causal cuts," which if I'm being honest, I don't feel were explained totally coherently in the paper. The essence though is that the cuts define dependency chains that allow the shim to decide when it's okay to `put`. It sounds based on the results that enabling the shim to use causal cuts resulted in fairly good results compared to the "pessimistic", conservative method, particularly when the commits consisted of series of short interactions (long chains created more complex dependencies and hurt throughput).

I suppose my question, then, is whether or not this technique has caught on? The idea of "more harmonious cross-layer coordination" as the authors refer to it, sounds nice, but I'm wondering if it's the kind of thing that's feasible for anyone smaller than Google or Amazon?
