---
layout: post
title:  Module Main has No Attribute... (on Pipelines and Pickles)
image:
  feature: pepper_crop.png
tags:   programming
date:   2019-03-07 11:01
---

It's no secret that the Data Science community is a fan of [scikit-learn](https://scikit-learn.org/stable/), *the* Python machine learning library that provides a common interface to dozens of machine learning models (well, hundreds of thousands, if you include all the hyperparameter options). But aside from the API, the useful feature extraction tools, and the sample datasets, two of the best things that scikit-learn has to offer are pipelines and (model-specific) pickles. Unfortunately, using pipelines and pickles together can be a bit tricky. I n this post I'll present a common problem that occurs when serializing and restoring scikit-learn pipelines, as well as a solution that I've found to be both practical and not hacky.

## Pipelines

If you're not familiar with scikit-learn [`Pipelines`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), they're definitely worth a look (I particularly like [Zac Stewart's post on them](http://zacstewart.com/2014/08/05/pipelines-of-featureunions-of-pipelines.html)). In essence, they (together with `FeatureUnions`) provide a method for sanely sequencing the stages of machine learning &mdash; from feature extraction to vectorization, normalization, dimensionality reduction, and modeling. Instead of a bunch of messy `fit_transforms` and `fit_predicts`, intermediate variables like "`x_vectorized`" or "`y_encoded`", and steps requiring a human-in-the-loop to execute them in the proper sequence, `Pipelines` allow us to execute these steps in one fell swoop:

```python
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

steps = [
  ('scl', StandardScaler()), 
  ('pca', PCA(n_components=2)),
  ('clf', DecisionTreeClassifier()
]

pipe = Pipeline(steps)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
```

## Custom Estimators and Transformers

Even better, scikit-learn exposes two classes, `BaseEstimator` and `TransformerMixin`, which allow us to create our own custom steps in our pipelines. Let's say we made a special transformer for text data, `TextNormalizer`, that implements the transformer interface:

```python
from sklearn.base import BaseEstimator, TransformerMixin


class TextNormalizer(BaseEstimator, TransformerMixin):
    """
    Do a bunch of fancy, specialized text normalization steps,
    like tokenization, part-of-speech tagging, lemmatization 
    and stopwords removal.
    """
    ...

    def normalize(self, document):
        # do the special stuff here

    def fit(self, X, y=None):
        return self

    def transform(self, documents):
        for document in documents:
            yield self.normalize(document)
```

Now we can use our `TextNormalizer` in a pipeline! Since we'll be using our custom text transformer to tokenize and tag our documents, we'll specify that our `TfidfVectorizer` not do any tokenization, preprocessing, or lowercasing on our behalf.

```python
from sklearn.feature_extraction import TfidfVectorizer
...

def identity(words):
    return words

steps = [
  ('norm', TextNormalizer()), 
  ('vect', TfidfVectorizer(
               tokenizer=identity, 
               preprocessor=None, 
               lowercase=False
               )
           ),
  ('clfr', LogisticRegression()
]

pipe = Pipeline(steps)
pipe.fit(train_docs, train_labels)
predicted_labels = pipe.predict(test_docs)
```

## Pickles

Now we want to save our model! Python's [pickle](https://docs.python.org/3/library/pickle.html) library gives us a way to do this, and scikit-learn has a specialized version of pickle called [joblib](https://scikit-learn.org/stable/modules/model_persistence.html) which provides some specialization for serializing fitted scikit-learn estimators and transformers.

If we want to serialize our first model from this post, the one that does scaling, then dimensionality reduction, and finally classification using a decision tree, we do it like this:

```python
from sklearn.externals import joblib

...

pipe.fit(X_train, y_train)
joblib.dump(pipe, 'scaled_tree_clf.pkl') 
```

And load it like this:

```python
fitted_model = joblib.load('scaled_tree_clf.pkl') 
```

We can pickle and load our custom text classification pipeline in the exact same way...

**EXCEPT!**

If we try to load the serialized model in a different project (let's say you have one library for testing and building models and a separate application for serving predictions), you might well see this:

```bash
AttributeError: module '__main__' has no attribute 'TextNormalizer'
```
or 

```bash
AttributeError: module '__main__' has no attribute 'identity'
```

What happened??

## Leaky Pipes


![Simple pipeline pickling](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2019-03-07-simple-pickle-pipeline.png)
![Problem pipeline pickling](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2019-03-07-problem-pickle-pipeline.png)
![Solved pipeline pickling](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2019-03-07-fixed-pickle-pipeline.png)



http://www.davidsbatista.net/blog/2018/02/28/TfidfVectorizer/
https://stackoverflow.com/questions/35201968/pickle-tfidfvectorizer-along-with-a-custom-tokenizer
https://tutel.me/c/programming/questions/49483732/why+does+my+flask+app+work+when+executing+using+python+apppy+but+not+when+using+heroku+local+web+or+flask+run
https://stackoverflow.com/questions/53167418/pickle-serialization-module-main-has-no-attribute-tokenize
https://www.stefaanlippens.net/python-pickling-and-dealing-with-attributeerror-module-object-has-no-attribute-thing.html
https://stackoverflow.com/questions/46077793/how-to-save-a-custom-transformer-in-sklearn
https://stackoverflow.com/questions/45106274/attributeerror-module-main-has-no-attribute-itemselector
https://stackoverflow.com/questions/54012769/saving-an-sklearn-functiontransformer-with-the-function-it-wraps