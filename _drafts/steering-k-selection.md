---
layout: post
title:  Steering K-Selection
date:   2017-04-07 12:19
---

In this post, I'll describe the use case and preliminary implementation of a new [Yellowbrick](http://www.scikit-yb.org) feature that enables the user to steer k-selection for k-means clustering.


## K-selection

Clustering models are unsupervised methods that attempt to detect patterns in unlabeled data. There are two primary classes of clustering algorithm: agglomerative clustering links similar data points together, whereas centroidal clustering attempts to find centers or partitions in the data. Yellowbrick provides the yellowbrick.cluster module to visualize and evaluate clustering behavior. Currently we provide two visualizers to evaluate centroidal mechanisms, particularly K-Means clustering, that help us to discover an optimal $K$ parameter in the clustering metric:

- Elbow Visualizer: visualize the clusters according to some scoring function, look for an "elbow" in the curve.
- Silhouette Visualizer: visualize the silhouette scores of each cluster in a single model.

Because it is very difficult to score a clustering model, Yellowbrick visualizers wrap Scikit-Learn "clusterer" estimators via their fit() method. Once the clustering model is trained, then the visualizer can call poof() to display the clustering evaluation metric.
