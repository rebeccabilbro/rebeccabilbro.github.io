---
layout: post
title:  Visual Diagnostics at Scale
image:
  feature: pepper_crop.png
tags:   proposals
date:   2019-02-04 11:15
---

Even with a modest dataset, the hunt for the most effective machine learning model is hard. Getting to that optimal combination of features, algorithm, and hyperparameters frequently requires significant experimentation and iteration. This lead some of us to stay inside algorithmic comfort zones, some to trail off on random walks, and others to resort to automated processes like gridsearch. But whatever the path we take, many of us are left in doubt about whether our final solution really is the optimal one. And as our datasets grow in size and dimension, so too does this ambiguity.

Fortunately, many of us have developed strategies for steering model search. Open source libraries like [seaborn](https://seaborn.pydata.org/), [pandas](https://pandas.pydata.org/) and [yellowbrick](https://www.scikit-yb.org/en/latest/) can help make machine learning more informed with visual diagnostic tools like histograms, correlation matrices, parallel coordinates, manifold embeddings, validation and learning curves, residuals plots, and classification heatmaps. These tools enable us to tune our models with visceral cues that allow us to be more strategic in our choices. Visualizing feature transformations, algorithmic behavior, cross-validation methods, and model performance allows us a peek into the multi-dimensional realm that our models operate. 

However, large, high-dimensional datasets can prove particularly difficult to explore. Not only do the majority of people struggle to visualize anything beyond two- or three-dimensional space, many of our favorite open source Python tools are not designed to be performant with arbitrarily big data. So how well *do* our favorite visualization techniques hold up to large, complex datasets? In this talk, we'll consider a suite of visual diagnostics &mdash; some familiar and some new &mdash; and explore their strengths and weaknesses in face of increasingly big data. Which suffer most from the curse of dimensionality? What are the workarounds (e.g. sampling, brushing, filtering, etc.) and when should we use them? How can we continue to steer the machine learning process &mdash; not only purposefully but at scale?


## Short Summary

The hunt for the most effective machine learning model is hard enough with a modest dataset, and much more so as our data grow! As we search for the optimal combination of features, algorithm, and hyperparameters, we often use tools like histograms, heatmaps, embeddings, and other plots to make our processes more informed and effective. However, large, high-dimensional datasets can prove particularly challenging. In this talk, we'll explore a suite of visual diagnostics, investigate their strengths and weaknesses in face of increasingly big data, and consider how we can steer the machine learning process, not only purposefully but at scale!


## Keywords

- machine learning
- statistical modeling
- visual diagnostics
- visualization
- big data
- high-dimensional data
- model selection
- data science