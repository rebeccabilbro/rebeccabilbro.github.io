---
layout: post
title:  Designing Democratic APIs
image:
  feature: pepper_crop.png
tags:   conference_proposals
date:   2019-12-18 10:42
---

When we set out to create the open source machine learning diagnostics library Yellowbrick, we were faced with tough decisions: will our users mostly be experienced ML practitioners or beginners? Should we prioritize ease of use or ease of contribution? How best to coordinate between the existing APIs of our two main dependencies, scikit-learn and Matplotlib? Here we walk through our decisions, including some of our biggest challenges, successes, and lessons learned along the way. 


# Democratic APIs: Balancing Hierarchy and Humanity in Pythonic Interface Design
by Rebecca Bilbro and Benjamin Bengfort

Building an open source library is not unlike building a democracy. The citizens of the programming community can freely choose whether or not to use the library, as well as how and whether to contribute back to the project. Meanwhile, the code of conduct lays out guidance that protects the rights of those citizens. As for governance, open source libraries are increasingly introducing mechanisms to enable different contributors and maintainers to cycle in and out of leadership roles. Finally, the API serves as a kind of rule-of-law, specifying how the library is to be used and providing direction as to how and where new components of the library can be integrated.   

The majority of resources on API design frame the problem in terms of object-oriented programming concepts; which behaviors to encapsulate, how to organize the hierarchy to enable shared behavior across classes, how to handle multiple inheritance, etc. However, it's often equally important to design around the citizenry of the project.

A key challenge of building an open source project is developing an API that serves a range of use cases, encourages a diversity of contributions, and can withstand the tests of time. When we set out to create the open source machine learning diagnostics library Yellowbrick, we were faced with tough decisions: will our users mostly be experienced ML practitioners or beginners? Should we prioritize ease of use or ease of contribution? How best to coordinate between the existing APIs of our two main dependencies, scikit-learn and Matplotlib? 

Ultimately, these decisions come down to the same challenge faced by any democracy &mdash; namely, that everyone wants power! In open source API design, the central tradeoff is of complexity, and complexity tends to be inversely proportional to control. Making an API easy *to use* requires developers to abstract away a tremendous amount of complexity &mdash; complexity which then makes it increasingly more difficult for users *to contribute*.

In this talk, we give a guided tour through the various checks and balances involved in the implementation of the Yellowbrick API. We walk through our decisions, including some of our biggest challenges, successes, and lessons learned along the way, in the hopes that our case study can help inform the creators of new libraries in the Python ecosystem!


# Outline
1. **Introduction (3 minutes)** 
- API design concepts: encapsulation, inheritance, class hierarchy, etc.
- Open source APIs: users, contributors, dependency management, change
- How the Yellowbrick API evolved (an animated commit history!)

2. **Balancing structure with flexibility (6 minutes)**
- What an API looks like from the user's perspective
- What an API looks like from the developer's perspective
- Balancing usability (consistency, flexibility) with hierarchy (multiple inheritance, shared functionality)
- Challenge: The evolution of the `ProjectionVisualizer` for principal components analysis and  manifold embeddings

3. **Balancing dependencies (6 minutes)** 
- `scikit-learn`: an object-oriented interface for machine learning
- `matplotlib.pyplot`: an object-oriented interface for creating plots
- Fitting `fig` and `ax` into `fit_predict` and `fit_transform`
- Challenge: Plotting recursive feature elimination with `RFECV`
- Best Practice: Keeping the dependencies set small 

4. **Balancing use cases (6 minutes)** 
- Building a tool for multiple use cases (experts and beginners)
- Challenge: Developing the `datasets` module
- Lesson Learned: Choosing `oneliners` over `VisualPipelines`

5. **Balancing contributor skill sets and backgrounds (6 minutes)** 
- The importance of multiple voices in open source development
- Why contributing to open source libraries is so hard
- Challenge: The `Visualizer` audit
- Best Practice: Scoping tasks and clearly defining "done" 

6. **Just plain balance! (1 minute)** 
- Balancing open source contribution with work, life, the universe, and everything!
- Lesson Learned: The Yellowbrick Governance Document

7. **Conclusion/Takeaways (2 minutes)** 
- Start with a team, or at least a partner, so  that you're integrating a diversity of thought *from the very beginning*
- Situate your API in an *ongoing community conversation*, including your future users and contributors
- Understand the *ecosystem of dependencies* that your API will inhabit
- Leverage *structure as orientation* to future contributors
- Plan for change with API *checks and balances* (like tests!)

# Who and Why (Audience)
This talk is geared towards intermediate programmers and data scientists, including those starting to develop their own APIs and those beginning to write code that others may use, maintain, and add onto. Prior experience with object-oriented programming concepts like encapsulation and inheritance will be helpful. No specific experience with scikit-learn, Matplotlib, or Yellowbrick is necessary, though users of those  libraries may be interested to learn more about the APIs of those projects! Audience members will learn about tradeoffs in open source API design and pick up some best practices and hard-won lessons from two humble OSS library creators/maintainers.


<!-- # Additional Notes
Ben and Rebecca are the creators of the open source, pure Python project Yellowbrick. Yellowbrick was first announced in a PyCon 2016 talk on [visual diagnostics for machine learning](https://youtu.be/c5DaaGZWQqY). Since then, Yellowbrick community members have delivered PyCon, PyData, and NumFOCUS talks across the US, in London, Spain, and Argentina, presented posters, run PyCon sprints, published [a paper](https://joss.theoj.org/papers/10.21105/joss.01075) in the Journal of Open Source Software (JOSS), and accumulated over 85 contributors from around the world and from people of all experience levels and backgrounds. 

Ben and Rebecca have presented posters, [talks](https://youtu.be/j1DdGX2d9BE), and [tutorials](https://www.youtube.com/watch?v=itKNpCPHq3I&feature=youtu.be) in past years of PyCon, as well as talks at PyData DC, PyData Carolinas, PyData NYC, PyData Argentina, PyData London, SciPy, and EuroSciPy. They are also adjunct faculty at Georgetown University's School of Continuing Studies in Washington, DC, where they teach in the Data Science Certificate Program (taught entirely in Python), and co-authors of [_Applied Text Analysis with Python_ (O'Reilly)](http://shop.oreilly.com/product/0636920052555.do). -->