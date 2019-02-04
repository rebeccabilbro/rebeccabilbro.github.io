---
layout: post
title:  Visual Diagnostics at Scale
image:
  feature: pepper_crop.png
tags:   proposals
date:   2019-02-04 11:15
---

Even with a modest dataset, the hunt for the most effective machine learning model is hard. Getting to that optimal combination of features, algorithm, and hyperparameters frequently requires significant experimentation and iteration. This lead some of us to stay inside algorithmic comfort zones, some to trail off on random walks, and others to resort to automated processes like gridsearch. But whatever the path we take, many of us are left in doubt about whether our final solution really is the optimal one. And as our datasets grow, so too does this ambiguity.

Fortunately, many of us have developed strategies for steering model search. Open source libraries like [seaborn](https://seaborn.pydata.org/), [pandas](https://pandas.pydata.org/) and [yellowbrick](https://www.scikit-yb.org/en/latest/) can help make machine learning more informed with visual diagnostic tools like histograms, correlation matrices, parallel coordinates, manifold embeddings, validation and learning curves, residuals plots, and classification heatmaps. These tools enable us to tune our models with visceral cues that allow us to be more strategic in our choices. Visualizing feature transformations, algorithmic behavior, cross-validation methods, and model performance allows us a peek into the multi-dimensional realm that our models operate. 

However, high-dimensional data can prove particularly difficult to explore. Not only do the majority of people struggle to visualize anything beyond two- or three-dimensional space, many of our favorite open source Python tools are not designed to be performant with arbitrarily large data. So how well *do* our favorite visualization techniques hold up to very large datasets? In this talk, we'll consider a suite of visual diagnostics &emdash; some familiar and some new &emdash; and explore their strengths and weaknesses in face of increasingly big data. Which suffer most from the curse of dimensionality? What are the workarounds (e.g. sampling, brushing, filtering, etc.) and when should we use them? How can we continue to steer the machine learning process &emdash; not only purposefully but at scale?
