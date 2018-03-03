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

```python
import nltk
import sqlite3

class SqliteCorpusReader(object):

    def __init__(self, path):
        self._cur = sqlite3.connect(path).cursor()

    def scores_albums_artists_texts(self):
        """
        Returns a generator with each review represented as a
        (score, album name, artist name, review text) tuple
        """
        sql = """
              SELECT S.score, L.label, A.artist, R.content
              FROM [reviews] S
              JOIN labels L ON S.reviewid=L.reviewid
              JOIN artists A on L.reviewid=A.reviewid
              JOIN content R ON A.reviewid=R.reviewid
              """
        self._cur.execute(sql)
        for score,album,band,text in iter(self._cur.fetchone, None):
            yield (score,album,band,text)
```


```python
import os
import nltk
import pickle
from slugify import slugify


class Preprocessor(object):
    """
    The preprocessor wraps a SqliteCorpusReader and manages the stateful
    tokenization and part of speech tagging into a directory that is stored
    in a format that can be read by the `PickledCorpusReader`. This format
    is more compact and necessarily removes a variety of fields from the
    document that are stored in Sqlite database. This format however is more
    easily accessed for common parsing activity.
    """
    def __init__(self, corpus, target=None, **kwargs):
        """
        The corpus is the `SqliteCorpusReader` to preprocess and pickle.
        The target is the directory on disk to output the pickled corpus to.
        """
        self.corpus = corpus
        self.target = target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, path):
        if path is not None:
            # Normalize the path and make it absolute
            path = os.path.expanduser(path)
            path = os.path.expandvars(path)
            path = os.path.abspath(path)

            if os.path.exists(path):
                if not os.path.isdir(path):
                    raise ValueError(
                        "Please supply a directory to write preprocessed data to."
                    )

        self._target = path

    def abspath(self, name):
        """
        Returns the absolute path to the target fileid from the corpus fileid.
        """
        # Create the pickle file extension
        fname  = str(name) + '.pickle'

        # Return the path to the file relative to the target.
        return os.path.normpath(os.path.join(self.target, fname))

    def tokenize(self, text):
        """
        Segments, tokenizes, and tags a document in the corpus. Returns a
        generator of paragraphs, which are lists of sentences, which in turn
        are lists of part of speech tagged words.
        """
        yield [
            nltk.pos_tag(nltk.wordpunct_tokenize(sent))
            for sent in nltk.sent_tokenize(text)
        ]

    def process(self, score_album_artist_text):
        """
        For a single file does the following preprocessing work:
            1. Checks the location on disk to make sure no errors occur.
            2. Gets all paragraphs for the given text.
            3. Segments the paragraphs with the sent_tokenizer
            4. Tokenizes the sentences with the wordpunct_tokenizer
            5. Tags the sentences using the default pos_tagger
            6. Writes the document as a pickle to the target location.
        This method is called multiple times from the transform runner.
        """
        score, album, artist, text = score_album_artist_text

        # Compute the outpath to write the file to.
        if album:
            name = album+'-'+artist
        else:
            name = artist
        target = self.abspath(slugify(name))
        parent = os.path.dirname(target)

        # Make sure the directory exists
        if not os.path.exists(parent):
            os.makedirs(parent)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )

        # Create a data structure for the pickle
        document = list(self.tokenize(text))
        document.append(score)

        # Open and serialize the pickle to disk
        with open(target, 'wb') as f:
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

        # Clean up the document
        del document

        # Return the target fileid
        return target

    def transform(self):
        """
        Transform the wrapped corpus, writing out the segmented, tokenized,
        and part of speech tagged corpus as a pickle to the target directory.
        This method will also directly copy files that are in the corpus.root
        directory that are not matched by the corpus.fileids().
        """
        # Make the target directory if it doesn't already exist
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        for score_album_artist_text in self.corpus.scores_albums_artists_texts():
            yield self.process(score_album_artist_text)
```

```python
if __name__ == '__main__':

    from reader import SqliteCorpusReader

    corpus = SqliteCorpusReader('../database.sqlite')
    transformer = Preprocessor(corpus, '../processed_review_corpus')
    docs = transformer.transform()
    print(len(list(docs)))
```


```python
import pickle
from nltk.corpus.reader.api import CorpusReader

PKL_PATTERN = r'(?!\.)[\w\s\d\-]+\.pickle'


class PickledReviewsReader(CorpusReader):
    def __init__(self, root, fileids=PKL_PATTERN, **kwargs):
        """
        Initialize the corpus reader
        """
        CorpusReader.__init__(self, root, fileids, **kwargs)

    def texts_scores(self, fileids=None):
        """
        Returns the document loaded from a pickled object for every file in
        the corpus. Similar to the SqliteCorpusReader, this uses a generator
        to achieve memory safe iteration.
        """
        for path, enc, fileid in self.abspaths(fileids, True, True):
            with open(path, 'rb') as f:
                yield pickle.load(f)

    def reviews(self, fileids=None):
        """
        Returns a generator of paragraphs where each paragraph is a list of
        sentences, which is in turn a list of (token, tag) tuples.
        """
        for text,score in self.texts_scores(fileids):
            yield text

    def scores(self, fileids=None):
        """
        Returns a generator of scores
        """
        for text,score in self.texts_scores(fileids):
            yield score
```

- Custom TextNormalizer to lemmatize and remove stop words

```python
import unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

class TextNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, language='english'):
        self.stopwords  = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()

    def is_punct(self, token):
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def normalize(self, document):
        return [
            self.lemmatize(token, tag).lower()
            for sentence in document
            for (token, tag) in sentence
            if not self.is_punct(token)
               and not self.is_stopword(token)
        ]

    def lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        return [
            ' '.join(self.normalize(doc)) for doc in documents
        ]
```


- use Numpy digitize method to naively bin the continuous target values


```python
import numpy as np

def documents(corpus):
    return list(corpus.reviews())

def continuous(corpus):
    return list(corpus.scores())

def categorical(corpus):
    """
    terrible : 0.0 < y <= 3.0
    okay     : 3.0 < y <= 5.0
    great    : 5.0 < y <= 7.0
    amazing  : 7.0 < y <= 10.1
    :param corpus:
    :return:
    """
    return np.digitize(continuous(corpus), [0.0, 3.0, 5.0, 7.0, 10.1])
```

## Preliminary Text Analytics Pipeline
- Build using Scikit-Learn Pipeline

```python
def train_model(path, model, cv=12):
    """
    Trains model from corpus at specified path; constructing cross-validation
    scores using the cv parameter and returning the scores.
    """
    corpus = PickledReviewsReader(path)
    X = documents(corpus)
    y = categorical(corpus)
    scores = cross_val_score(model, X, y, cv=cv)

    return scores

if __name__ == '__main__':
    from sklearn.pipeline import Pipeline
    from sklearn.neural_network import MLPClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer

    corpus_path = '../processed_review_corpus'

    pipeline = Pipeline([
        ('norm', TextNormalizer()),
        ('tfidf', TfidfVectorizer()),
        ('ann', MLPClassifier(hidden_layer_sizes=[500,150], verbose=True))
    ])

    scores = train_model(corpus_path, pipeline)
```

- use ConfusionMatrix to visually evaluate
- use ClassBalance to visualize imbalance
- talk through selection bias - why initial bins didn’t work

## Tuning Bins with ClassBalance
- redo with better distributed bins for target values
- (hopefully) show better results

## Conclusion/Teaser for New ClassBalanceHeatmap Visualizer
- how to combine insight from ConfusionMatrix with interpretability of ClassBalance?
