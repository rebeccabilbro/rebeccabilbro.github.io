---
layout: post
title:  Pop Distributed Systems
image:
  feature: pepper_crop.png
tags:   dist_sys
date:   2019-02-08 10:07
---

This past Fall, I took a course in distributed systems at the University of Maryland College Park. As someone working in software development but who didn't study computer science in school, I went into this class with less of a theoretical and more of an applied understanding of reliability, scalability, and maintainability. I also had a healthy skepticism about the buzzwords that characterize most conversations in industry about the latest tools and techniques. Having now finished the class and covered topics from eventually consistent systems to distributed consensus algorithms and many in between, I thought it would be interesting to revisit reliability, scalability, and maintainability from an industry perspective by reading Martin Kleppmann's book Designing Data Intensive Applications. In this post I'll discuss some takeaways and favorite quotes from the first part of the book.

>>> The buzzwords that fill this space are a sign of enthusiasm for the new possibilities, which is a great thing. However, as software engineers and architects, we also need to have a technically accurate and precise understanding of the various technologies and their trade-offs if we want to build good applications. For that understanding, we have to dig deeper than buzzwords. - Martin Kleppmann

## Chapter 1

>> And it can be hard to combine tools when you need to do something that a single tool cannot do alone.

Most tools do more than one thing even if they were designed or are intended to do one specific thing best (e.g. Redis v. Kafka for persisting data and passing messages around). It is unlikely that a specific application can be made with only a single tool, so you have to cobble together several that may have seemingly overlapping capabilities.

>> a fault is not the same as a failure

Reliability vs fault-tolerance are presented as nearly equivalent, though this is a bit of a misrepresentation if we're talking (as we seem to be) about reliability at the level of the entire system; in an academic context, fault-tolerance has a more specific usage, meaning the tolerance of the data storage layer in particular to faults like weather disasters or byzantine incursions. 

>> it is meaningless to say “X is scalable” or “Y doesn’t scale.” Rather, discussing scalability means considering questions like “If the system grows in a particular way, what are our options for coping with the growth?” and “How can we add computing resources to handle the additional load?”

Scaling isn't something that you just do once.
The example of Twitter is a good one; they initially used a timeline model that suffered from fan-out, pivoted to a different model that made timelines cheaper but posting more expensive, and finally have had to scale again with a combination of the first two models. 

>> When you increase a load parameter and keep the system resources (CPU, memory, network bandwidth, etc.) unchanged, how is the performance of your system affected? When you increase a load parameter, how much do you need to increase the resources if you want to keep performance unchanged?

These are good, concrete questions to ask to figure out what will happen to your application as load increases.

>> The architecture of systems that operate at large scale is usually highly specific to the application—there is no such thing as a generic, one-size-fits-all scalable architecture (informally known as magic scaling sauce). The problem may be the volume of reads, the volume of writes, the volume of data to store, the complexity of the data, the response time requirements, the access patterns, or (usually) some mixture of all of these plus many more issues.

The anxiety of the apps developer is the stress of trying to decide how to cobble together tools that may have seemingly overlapping cababilities, with the knowledge that some of these tools will be leveraged in ways that scale poorly, but without always knowing in advance where those growing pains will manifest.