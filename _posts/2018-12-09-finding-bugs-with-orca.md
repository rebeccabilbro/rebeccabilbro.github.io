---
layout: post
title:  Finding Needles in Haystacks with Orca
image:
  feature: pepper_crop.png
date:   2018-12-09 14:17
tags:   class_readings
---

While batching in distributed systems is great for performance, it adds complexity and can make diagnostics tough. For example, trying to find a small error inside a file inside a commit that has been aggregated together with many other commits is a needle-in-haystack problem. [Orca](https://www.microsoft.com/en-us/research/uploads/prod/2018/10/Orca-OSDI.pdf) is a search engine for finding such needles. 

Orca is designed to take as input the text describing the symptoms of the bug, and to return as output a list of potentially offending commits, ranked in order of the predicted probability that the commit contains the bug. 

First the text is normalized (removing stopwords) and vectorized with a variant of term-frequency inverse-document frequency that they call TF-IQF. Next a provenance graph is built to find relevant builds, then differential code analysis is used to whittle down the commit search space. 

The provenance graph is designed to create the initial search space, creating a way to explore commits over time and across builds. Once a set of candidate commits have been identified, differential code analysis is used to prune the search space, using abstract syntax trees (AST) of both versions of a file to get the diff, focusing on differences in classes, methods, references, conditions, and loops. While this method is subject to false positives, it does effectively limit the total search space.

Then for each commit, Orca uses TF-IQF to score every token that appears in the diffs, then computes composite scores for every file, aggregates the file scores to the level of the commit, and returns the commits, reverse-sorted by their aggregate TF-IQF score. 

I think that the solution of using the problem descriptions as the search text is cool (i.e. could easily be integrated into a chat bot app), but also a bit naive, since it assumes that people will generally be good at describing problems (rare in my observation), and that symptoms will be straightforward. However, as a semi-professional Office 365 hater, I have to admit that it was cool to read about how the Microsoft team is using machine learning for things like bug detection in their distributed services.