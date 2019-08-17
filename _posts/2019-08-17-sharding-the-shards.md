---
layout: post
title:  Sharding the Shards
image:
  feature: pepper_crop.png
tags:   dist_sys
date:   2019-08-17 14:05
---

In "Sharding the Shards: Managing Datastore Locality at Scale with Akkio", Annamalai, et al. present Akkio, a locality management service that can be tacked on to an application (like a social media platform) its distributed datastore to strategically migrate data to the places where it is being accessed. The premise of Akkio is that for a subset of applications, data access is going to be much more related to locality (specifically the locations of the users who are going to access the data) than it is by other metadata features like time (e.g. how recent the social media post is) or type (e.g. whether the content is a picture or a video). Essentially, Akkio tracks accesses to determines how to distribute data and when to move it around. From a business standpoint, the goals of Akkio are to (1) improve the user experience by reducing app response time and (2) to make the backend more efficient, avoiding expensive caching schemes (or even worse, the cost of full replication for an enormous amount of data) and better adapting to shifting access patterns as daylight hours shift across the globe. 


## Data Neighborhoods

Distributed data storage generally requires that we make decisions about breaking the data down into smaller more manageable pieces (aka shards) that can be written, replicated, accessed, and even moved. However, one of the main insights of the Akkio paper is that the level of granularity that best serves writing and replication may be too large to effectively serve dynamic accesses and data migration.

The authors introduce the `μ-shard`, which is a collection of data that is likely to be accessed by the same datacenters, and that makes sense to migrate as one bundle. As such, the `μ-shard` becomes a kind of atom of data migration in Akkio, since one `μ-shard` is guaranteed to be fully contained by a single shard.

While most systems have a backend chunkserver-like application that is responsible sharding data via some key partitioning or hashing algorithm, for `μ-sharding` Akkio requires that the frontend application provide data about locality and mutual access probabilities that can be used to determine which pieces of data should be grouped together into a `μ-shard`. Then, Akkio can assign the `μ-shard` to a shard that has the appropriate replication and consistency requirements for the `μ-shard`.


## Thoughts, Questions, and Concerns

The authors suggest Akkio is targeted mostly at write-heavy workloads, meaning that it is not well-suited to social graph data, but I am curious about how the integration of Akkio could impact social networks that are not defined by geographic localities, or that exist across several geographically disparate regions.