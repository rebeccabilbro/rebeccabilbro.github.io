---
layout: post
title:  Subplots with Yellowbrick
image:
  feature: pepper_crop.png
tags:   programming
date:   2020-06-08 11:45
---

In this quick post, we'll see how to use Yellowbrick together with Matplotlib's subplots feature to create a visual story about the modeling process:

![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2020-06-08-confusion-matrix-cv-scores.png)


# Creating the subplots

First we have to use Matplotlib's [subplots feature](https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html) to create a figure that will be able to contain two side-by-side subplots:

```python
fig, axes = plt.subplots(ncols=2)
```

This will create a `fig` object, which is the entire space of our plot, as well as an `axes` object, which contains two `ax` objects that we will be able to access separately with numerical indexing.

_Note: If we had written `plt.subplots(nrows=2, ...)` we'd get two plots stacked on top of each other instead of side-by-side._

# Confusion Matrix

The Yellowbrick [`ConfusionMatrix` visualizer](https://www.scikit-yb.org/en/develop/api/classifier/confusion_matrix.html) is designed to help us understand where our model is making mistakes in classifying the training data. Because the visualizer accepts an `ax` parameter, we can pass in the coordinates of our first `ax` object directly into the visualizer on instantiation to tell it to position itself inside those coordinates on the figure we've created above.

```python
confusion_matrix = ConfusionMatrix(
    model,
    ax=axes[0]
)
```

# Cross-Validation

The Yellowbrick [`CVScores` visualizer](https://www.scikit-yb.org/en/develop/api/model_selection/cross_validation.html) is part of the `model_selection` module, and is aimed at helping us to validate that our model is performing about equally well on all slices of our data during cross-validation. The `CVScores` visualizer also accepts an `ax` parameter:

```python
cv_scores = CVScores(
    model,
    ax=axes[1],
    scoring="f1_weighted",
    cv=StratifiedKFold(n_splits=12, shuffle=True)
)
```

This code tells Yellowbrick to put the `CVScores` plot into the second of the two axes we created.

# Putting all the pieces together

Here are all the pieces, put together (with a few other stylistic additions):

<script src="https://gist.github.com/rebeccabilbro/797521107bbe5070f511aa6c5a290e0c.js"></script>

Note that in the above, we also use Matplotlib's [`tight_layout` method](https://matplotlib.org/3.2.1/tutorials/intermediate/tight_layout_guide.html) to encourage all of the features of the subplots to fit together nicely inside the figure. It's very helpful when using many subplots! Check out [this post](https://www.scikit-yb.org/en/develop/matplotlib.html) for more examples of how to use Matplotlib effectively!