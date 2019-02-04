---
layout: post
title:  Visual Diagnostics at Scale
image:
  feature: pepper_crop.png
tags:   machine_learning
date:   2019-02-04 11:15
---

## High Dimensional Information Visualization

With the rise of big data comes the need for better data visualization tools. What role do visual analytics play in data science workflows and data products? How can visualizations be implemented with textual analytics and natural language processing? How can we represent massive amounts of data and employ visualizations to overcome the curse of dimensionality?

Multi-dimensional data can prove to be particularly difficult to explore because the majority of people struggle to visualize anything beyond two- or three-dimensional space. But, with the right tools, highly complex, even multi-dimensional data can be made to feel intuitive. 

Moreover, sophisticated approaches like graphs, clusters, treemaps, and interactive visualizations that go beyond simple histograms and scatter plots can also lead us to new, previously undiscovered insights about all kinds of data. This project will build on recent publications in visual analytics and explore cutting-edge implementations combining mathematical algorithms, Python programming, and principles of design.

## Visual Diagnostics

Machine learning is ultimately a search for the best combination of features, algorithm, and hyperparameters that result in the best performing model. Oftentimes, this leads us to stay in our algorithmic comfort zones, or to resort to automated processes such as grid searches and random walks. Whether we stick to what we know or try many combinations, we are sometimes left wondering if we have actually succeeded.

By enhancing model selection with visual diagnostics, data scientists can inject human guidance to steer the search process. Visualizing feature transformations, algorithmic behavior, cross-validation methods, and model performance allows us a peek into the high dimensional realm that our models operate. As we continue to tune our models, trying to minimize both bias and variance, these glimpses allow us to be more strategic in our choices. The result is more effective modeling, speedier results, and greater understanding of underlying processes.

Visualization is an integral part of the data science workflow, but visual diagnostics are directly tied to machine learning transformers and models. The Yellowbrick library extends the scikit-learn API providing a Visualizer object, an estimator that learns from data and produces a visualization as a result. In this tutorial, we will explore feature visualizers, visualizers for classification, clustering, and regression, as well as model analysis visualizers. We'll work through several examples and show how visual diagnostics steer model selection, making machine learning more informed, and more effective.