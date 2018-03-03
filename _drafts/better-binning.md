---
layout: post
title:  Better Binning for Classification Problems: Creating Categorical Values from Continuous Values
date:   2018-03-03 13:05
---

Ever had the problem of having to convert a continuously-valued target array into bins for classification? In this post, I'll walk through a case study, starting with a naive approach and moving to a more informed strategy using the visual diagnostics library [Yellowbrick](http://www.scikit-yb.org).


## Premise
- A lot of machine learning problems in the real world suffer from the curse of dimensionality; you have fewer training instances than you’d like, and predictive signal is distributed (often unpredictably!) across many different features.
- One example is when your target is continuously-valued, but there aren’t enough instances to predict these values to the precision of regression.
- What if we transform the regression problem into a classification problem? We can try to do this by binning the continuous values into buckets for classification. But how do we pick the bins?

## Dataset Intro
- About the Pitchfork album reviews corpus - funny! snarky! sentiment analysis??
- Download the data from https://www.kaggle.com/nolanbconaway/pitchfork-data/data
- Custom CorpusReader to access the text and scores
- Custom TextNormalizer to lemmatize and remove stop words
- use Numpy digitize method to naively bin the continuous target values

## Preliminary Text Analytics Pipeline
- Build using Scikit-Learn Pipeline
- use ConfusionMatrix to visually evaluate
- use ClassBalance to visualize imbalance
- talk through selection bias - why initial bins didn’t work

## Tuning Bins with ClassBalance
- redo with better distributed bins for target values
- (hopefully) show better results

## Conclusion/Teaser for New ClassBalanceHeatmap Visualizer
- how to combine insight from ConfusionMatrix with interpretability of ClassBalance?
