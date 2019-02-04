---
layout: post
title:  Visual Diagnostics at Scale
image:
  feature: pepper_crop.png
tags:   proposals
date:   2019-02-04 11:15
---

Even with a modest dataset, the hunt for the most effective machine learning model is hard. Getting to that optimal combination of features, algorithm, and hyperparameters requires  experimentation and iteration. This can lead us to stay inside algorithmic comfort zones, to trail off on random walks, and to resort to automated processes like gridsearch. Whatever path we take, we're often left in doubt about whether our final solution really is the optimal one. As our datasets grow, so too does this ambiguity.

Fortunately, many of us have developed strategies for steering our search process. Open source libraries like [scikit-learn](https://scikit-learn.org/stable/), [seaborn](https://seaborn.pydata.org/), and [scikit-yellowbrick](https://www.scikit-yb.org/en/latest/) can help make machine learning more informed, and more effective. In particular, visual diagnostics enable us to tune our models with visceral cues that allow us to be more strategic in our choices. The result is more effective modeling, speedier results, and greater understanding of underlying processes.

Visualizing feature transformations, algorithmic behavior, cross-validation methods, and model performance allows us a peek into the high dimensional realm that our models operate. On the other hand, multi-dimensional data can prove particularly difficult to explore. Not only do the majority of people struggle to visualize anything beyond two- or three-dimensional space, many of our favorite open source tools are not designed to be performant with arbitrarily large data. So how well *do* our favorite visualization techniques hold up to very large datasets? In this talk, we'll explore a suite of visual diagnostics &emdash; some familiar and some new &emdash; and consider their strengths and weaknesses in face of increasingly big data. Which suffer most from the curse of dimensionality? What are the workarounds (e.g. sampling, brushing, filtering, etc.) and when should we use them? How can we continue to steer the machine learning process at scale?
