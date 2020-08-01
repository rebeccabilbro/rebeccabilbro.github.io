---
layout: post
title:  Thrify Machine Learning
image:
  feature: pepper_crop.png
tags:   proposals
date:   2020-08-01 11:55
---

We live with an abundance of ML resources; from open source tools, to GPU workstations, to cloud-hosted autoML. What's more, the lines between AI research and everyday ML have blurred; you can recreate a state-of-the-art model from arxiv papers at home. But can you afford to? In this post, we explore ways to recession-proof your ML process without sacrificing on accuracy, explainability, or value.

## Thrifty Machine Learning

The variety of resources for machine learning is truly astounding; from open source libraries (Tensorflow, Keras, PyTorch, scikit-learn, Spark) to commercially available GPU-accelerated workstations, to convenient cloud-hosted autoML toolkits. What's more, the lines between the AI research community and everyday ML practitioners has blurred &mdash; meaning that, at least theoretically, any one of us could recreate a state-of-the-art model from arxiv papers at home or work. But can we afford to?

Here are my best practices to recession-proof the machine learning process without sacrificing on accuracy, explainability, or value:

1. *Introduction*: Machine learning today is an embarrassment of riches! But, times are tough, jobs are getting cut, VC funding is drying up, and we're all going to be facing tough times. We have to figure out how to be productive, creative, and thoughtful machine learning practitioners in the lean times ahead.
2. *Build it yourself*: Don't outsource your ML to a blackbox, even if it seems convenient and allows your team to skip the code reviews. Machine learning as a service (MLaaS) is just repackaging & upselling the open source tools. And then you can't even tune your models!
3. *Label your own data*:  No, cutting coupons isn't glamorous either, but it does save money.
4. *Start small*: Pick simple models first, filter out the weak performers, and only tune the best. Move towards complexity gradually and purposefully.
5. *Be objective*: Let your data decide which model is best, not Twitter/LinkedIn/Medium/arxiv.
6. *Start local*: Build on your laptop first, downsampling the data if necessary. Use cloud for production only.
7. *Serialize everything*: Don't just pickle the model, pickle engineered features, lexicons, and other artifacts, too. Save diagnostic plots and other metadata together with the models.
8. *Define done*: Whether that's determining if an F1>0.7 is realistic, or a 20% reduction in MSE is possible, or knowing when to fold; establish clear limits and action points to decide when (or whether) to keep tuning.

Remember, it's necessity, not abundance, who is the mother of invention; when we shift our collective mindset toward model thriftiness rather than just model performance, there's no telling what new things we'll discover...