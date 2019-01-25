---
layout: post
title:  Converting Python 2 Pickles to Python 3
image:
  feature: pepper_crop.png
tags:   programming
date:   2019-01-25 10:06
---

Happy New Year and welcome to 2019, the [final year of Python 2 support](https://pythonclock.org/)! In honor of the new year, here's a short post on how to convert pickles from your legacy Python 2 codebase to Python 3.


## Encoding Issues

The first issue you're likely to encounter is an encoding issue:

```python
import pickle

with open("old_pickle.pkl", 'rb') as f:
    loaded = pickle.load(f) 
```

```bash
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0x95 in position 0: ordinal not in range(128)
```

This is because pickle's [default](https://docs.python.org/3/library/pickle.html#pickle.load) is to decode all string data as ascii, which fails in this case. Instead we have to convert Python 2 bytestring data to Python 3 using either `encoding="bytes"`, or for pickled NumPy arrays, Scikit-Learn estimators, and instances of `datetime`, `date` and `time` originally pickled using Python 2, `encoding="latin1"`. More on this [here](https://stackoverflow.com/questions/28218466/unpickling-a-python-2-object-with-python-3/28218598#28218598).

#### Solution
``` python
with open("old_pickle.pkl", 'rb') as f:
    loaded = pickle.load(f, encoding="latin1") 
```
or
``` python
with open("old_pickle.pkl", 'rb') as f:
    loaded = pickle.load(f, encoding="bytes") 
```

## Python 2 Objects vs Python 3 Objects

The next problem you might encounter is a `KeyError`, when Python 3 pickle fails to recognize the key `b'ObjectType'` from the Python 2 pickle:

```python
with open("old_pickle.pkl", "rb") as f:
    loaded = pickle.load(f, encoding="latin1")
```

```bash
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/dill/_dill.py", line 568, in _load_type
    return _reverse_typemap[name]
KeyError: b'ObjectType'
```

#### Solution

This occurs because the `ObjectType` type was removed in Python 3. The solution is to use the `dill` library to recast the Python 2 `ObjectType` to a Python 3 `object`:

``` python
import dill

dill._dill._reverse_typemap['ObjectType'] = object
```

More on this [here](https://stackoverflow.com/questions/42960637/python-3-5-dill-pickling-unpickling-on-different-servers-keyerror-classtype) and [here](https://stackoverflow.com/questions/52687577/error-keyerror-objecttype-when-loading-pickle).


## From the Command Line

Here's a little command line application I use for quickly converting these legacy pickles over to Python 3:

<script src="https://gist.github.com/rebeccabilbro/2c7bb4d1acfbcdcf9156e7b9b7577cba.js"></script>


## Gotchas and Addenda

### Scikit-Learn-Specific Issues

Be warned that you may still get library-specific warnings, for instance when we try to unpickle an old version of a Scikit-Learn estimator using a newer version of the library:

```bash
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/sklearn/base.py:251: UserWarning: Trying to unpickle estimator TfidfTransformer from version 0.20.2 when using version 0.20.1. This might lead to breaking code or invalid results. Use at your own risk.
  UserWarning)
```

### Spyder-Specific Issues

Additionally, if you're dealing with a case where you're extracting pickles from a pickled Spyder session, you'll have to use `dill` to load the session first, then load the individual pickles, then save those pickles individually, so that they can be used outside of a Spyder console:

```python
import dill
import pickle

## load the session, which has everything locked in
dill.load_session("session_pickle.pkl")

## Load the actual pickles
[classifier, count_vectorizer, tfidf_transformer] = pickle.loads(model_components)

## Save the pickles individually
with open("classifier_p2.pkl", "wb") as x:
    pickle.dump(classifier, x)

with open("count_vectorizer_p2.pkl", "wb") as y:
    pickle.dump(count_vectorizer, y)

with open("tfidf_transformer_p2.pkl", "wb") as z:
    pickle.dump(tfidf_transformer, z)

```

Once you've done this, you can go ahead and convert the individual Python 2 pickles over to Python 3.