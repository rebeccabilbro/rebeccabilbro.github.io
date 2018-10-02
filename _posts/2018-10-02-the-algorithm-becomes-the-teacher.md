---
layout: post
title:  The Algorithm Becomes the Teacher
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-10-02 14:43
---

What if the value of new scientific contributions was measured not in novelty or performance, but in understandability? This question, raised in ["In Search of an Understandable Consensus Algorithm,"](http://files.catwell.info/misc/mirror/raft/raft.pdf) for me calls to mind Richard Feynman's approach to learning and teaching; namely, that if you couldn't explain an advanced principle of Physics to a freshman, you didn't really understand it yet yourself.

In the case of the Raft paper, the goal is to make consensus understandable, reasoning that people are more likely to teach and use algorithms they actually understand. Ongaro and Ousterhout describe their creation of a new algorithm for consensus in distributed systems intended not to beat Paxos on grounds of speed or throughput, but only in its coherence. The results will shock you! Just kidding; Raft is demonstrably more understandable than Paxos, if somewhat non-standard in its empirical arguments. The central insight of the paper is that understandability is just a good a reason to develop, teach, and implement algorithms as are performance and novelty, and perhaps even better.

> Feynman was a truly great teacher. He prided himself on being able to devise ways to explain even the most profound ideas to beginning students. Once, I said to him, "Dick, explain to me, so that I can understand it, why spin one-half particles obey Fermi-Dirac statistics." Sizing up his audience perfectly, Feynman said, "I'll prepare a freshman lecture on it." But he came back a few days later to say, "I couldn't do it. I couldn't reduce it to the freshman level. That means we don't really understand it." -- _[Feynman's Lost Lecture](https://www.amazon.com/Feynmans-Lost-Lecture-David-Goodstein/dp/0393319954)_ by David and Judith Goodstein

## Understanding the Problem

One helpful part of the paper was the discussion about what it is specifically that makes Paxos so difficult to understand and reason about. According to the authors, it comes down to the single-decree protocol, essentially the base case for having a single value accepted in a distributed system. Paxos' defining characteristics are that it doesn't necessarily require a strong, stable leader and that leadership election is implicit. The consequences are that there are many types of messages that need to get passed back and forth between replicas (e.g. propose, promise, commit, ack, nack, etc) and potential states of consistency that must be accounted for. But these all add an enormous amount of complexity.

By contrast, Raft embraces strong leadership, making leader election explicit, and specifying that leaders are append only and log entries only flow in a single direction. In essence, there is much less negotiation that needs to happen in Raft. This also means that there are only a few types of states of inconsistencies that we need to worry about, namely (1)"A follower may be missing entries that are present on the leader", (2) "it may have extra entries that are not present on the leader", (3) "or both" or (4) "Missing entries in a log may span multiple terms." This makes discouraging, detecting, and resolving inconsistencies a lot more straightforward.

## Clocks

I thought the authors made some interesting choices around timing and clocks. For instance, they chose "terms" as the units for the system's logical clock; this means you can easily compare two logs to see which is more up-to-date "comparing the index and the term of [their] last entries...[if they have] different terms, the one with the later term is more up-to-date. If the logs end with the same term, then whichever log is longer is more up-to-date." Though other implementations have mentioned heartbeats, I liked that the Raft paper specified their construction (e.g. empty append messages) and articulated what they were useful for (e.g. to prevent leadership coups). Moreover, I though the randomized election timeouts were a clever way of reducing the likelihood of split votes, particularly since it turned out that only a small amount of difference was needed to have good results. Finally, I liked the choice of setting broadcast time at an order of magnitude less than election timeout, which I found reminiscent of the sequence number boosting used in "Paxos Made Live," which was used to avoid master churn.


## User Study

One thing that certainly stands out a lot about this paper is the user study results. The authors explicitly asked questions like "How easily were students able to learn Raft v. Paxos, controlling somewhat for ordering and prior knowledge?" and "How did students subjectively rate Raft v. Paxos, in terms of understandability and implementability?"

The measure of success here is quite different than in previous papers. The Paxos and ePaxos are examples of papers written by academic researchers with the goal of advancing science, not industry. The measures of success are novelty and experimental throughput and latency results. By contrast, "Paxos Made Live" is an industry paper, written by a commercial R&D team with the goal of advancing the product. The measure of success is how hard it is to implement, how successfully it performs in production, and (eventually) how much of a pain it is to maintain the system over time. The Raft paper, however, appears to be written by teacher-researchers, with the goal of explaining concurrency to their students. As such they seem less interested in advancing science directly (they don't show experimental latency or throughput results) and more interested in whether the algorithm can be assigned to students as a project (who will then, hopefully, go on to do great things). A different, but refreshing, approach.
