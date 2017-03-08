---
layout: post
title:  Colorizing text based on part-of-speech tags
date:   2017-03-07 18:00
---

In this post, I'll describe the use case and preliminary implementation of a new [Yellowbrick](http://www.scikit-yb.org) feature that enables the user to print out colorized text that illustrates different parts-of-speech.


## Part-of-speech tagging

Under the hood, the majority of NLP-based applications work in the same fundamental way; they take in text data as input, parse it into composite parts, compute upon those composites, and then recombine them to deliver a meaningful and tailored end result.

To transform a raw text corpus into data that can be used for modeling, there are five things that need to happen first: content extraction, paragraph blocking, sentence segmentation, word tokenization, and part-of-speech tagging. This means that part-of-speech tagging is a critical component in many natural language processing activities.

Once you have broken the documents down in to paragraphs, the paragraphs into sentences, and the sentences into tokens, you need to tag each token with the it's appropriate part of speech.

Parts of speech (e.g. verbs, nouns, prepositions, adjectives) indicate how a word is functioning within the context of a sentence. In English as in many other languages, a single word can function in multiple ways, and we would like to be able to distinguish those uses (for example the words "ship" and "shop" can be either a verb, or a noun, depending on the context). Part-of-speech tagging lets us encode information not only about a word's definition, but also its use in context.

If you're using NLTK, the off-the-shelf part-of-speech tagger, [`pos_tag`](https://github.com/nltk/nltk/blob/develop/nltk/tag/__init__.py), uses the +PerceptronTagger()+ and the Penn Treebank tagset (at least it does at the time of this writing).

The [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) consists of 36 parts of speech, structural tags, and indicators of tense (+NN+ for singular nouns, +NNS+ for plural nouns, +JJ+ for adjectives, +RB+ for adverbs, +PRP+ for personal pronouns, etc.).


## Existing tools

Text colorizer, inspired by Termcolor
https://github.com/Parallel-in-Time/PararealF90/tree/master/termcolor-1.1.0



## The components of a part-of-speech colorizer

The goal is to enable visual part-of-speech tagging. In particular, I envisioned the `PosTagVisualizer()` as a simple utility that would let Yellowbrick users visualize the proportions of nouns, verbs, etc. and to use this information to make decisions about text normalization (e.g. stemming vs lemmatization) and vectorization.


### Building a ANSI colormap
```python
COLORS = {
    'white'      : "\033[0;37m{}\033[0m",
    'yellow'     : "\033[0;33m{}\033[0m",
    'green'      : "\033[0;32m{}\033[0m",
    'blue'       : "\033[0;34m{}\033[0m",
    'cyan'       : "\033[0;36m{}\033[0m",
    'red'        : "\033[0;31m{}\033[0m",
    'magenta'    : "\033[0;35m{}\033[0m",
    'black'      : "\033[0;30m{}\033[0m",
    'darkwhite'  : "\033[1;37m{}\033[0m",
    'darkyellow' : "\033[1;33m{}\033[0m",
    'darkgreen'  : "\033[1;32m{}\033[0m",
    'darkblue'   : "\033[1;34m{}\033[0m",
    'darkcyan'   : "\033[1;36m{}\033[0m",
    'darkred'    : "\033[1;31m{}\033[0m",
    'darkmagenta': "\033[1;35m{}\033[0m",
    'darkblack'  : "\033[1;30m{}\033[0m",
    'off'        : "\033[0;0m{}\033[0m"
}
```

### Mapping the ANSI colors to the Penn Treebank Tags

```python
tag_map = {
    'NN'   : 'green',
    'NNS'  : 'green',
    'NNP'  : 'green',
    'NNPS' : 'green',
    'VB'   : 'blue',
    'VBD'  : 'blue',
    'VBG'  : 'blue',
    'VBN'  : 'blue',
    'VBP'  : 'blue',
    'VBZ'  : 'blue',
    'JJ'   : 'red',
    'JJR'  : 'red',
    'JJS'  : 'red',
    'RB'   : 'cyan',
    'RBR'  : 'cyan',
    'RBS'  : 'cyan',
    'IN'   : 'darkwhite',
    'POS'  : 'darkyellow',
    'PRP$' : 'magenta',
    'PRP$' : 'magenta',
    'DT'   : 'black',
    'CC'   : 'black',
    'CD'   : 'black',
    'WDT'  : 'black',
    'WP'   : 'black',
    'WP$'  : 'black',
    'WRB'  : 'black',
    'EX'   : 'yellow',
    'FW'   : 'yellow',
    'LS'   : 'yellow',
    'MD'   : 'yellow',
    'PDT'  : 'yellow',
    'RP'   : 'yellow',
    'SYM'  : 'yellow',
    'TO'   : 'yellow',
}
```


### A function to colorize the text

```python
def colored(text, color=None):
    """
    Colorize text
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        if color is not None:
            text = COLORS[color].format(text)
    return text
```

### Now in the if-main statement

```python

import os
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize

text = """In a small saucepan, combine sugar
          and eggs until well blended. Cook
          over low heat, stirring constantly,
          until mixture reaches 160° and coats
          the back of a metal spoon. Remove
          from the heat. Stir in chocolate and
          vanilla until smooth. Cool to
          lukewarm (90°), stirring occasionally.
          In a small bowl, cream butter until
          light and fluffy. Add cooled
          chocolate mixture; beat on high speed
          for 5 minutes or until light and
          fluffy. In another large bowl, beat
          cream until it begins to thicken. Add
          confectioners' sugar; beat until stiff
          peaks form. Fold into chocolate
          mixture. Pour into crust. Chill for at
          least 6 hours before serving. Garnish
          with whipped cream and chocolate curls
          if desired."""

# Tokenize the text
tokens = word_tokenize(text)

# Part of speech tag the text and map to Treebank-tagged colors
tagged = [
  (tag_map.get(tag),token)
  for token, tag in pos_tag(tokens)
]
print(' '.join(
  (colored(token, color)
  for color, token in tagged)))
```


![french silk pie](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-03-07-french-silk.png)


![algebra from wikipedia](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-03-07-algebra.png)


![nursery rhyme](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-03-07-nursery-rhyme.png)


### Conforming to the Yellowbrick API

```python
from yellowbrick.text.base import TextVisualizer

class PosTagVisualizer(TextVisualizer):
    """
    A part-of-speech tag visualizer colorizes text to enable
    the user to visualize the proportions of nouns, verbs, etc.
    and to use this information to make decisions about text
    normalization (e.g. stemming vs lemmatization) and
    vectorization.

    Parameters
    ----------
    kwargs : dict
        Pass any additional keyword arguments to the super class.
    cmap : dict
        ANSII colormap

    These parameters can be influenced later on in the visualization
    process, but can and should be set as early as possible.
    """
    def __init__(self, ax=None, **kwargs):
        """
        Initializes the base frequency distributions with many
        of the options required in order to make this
        visualization work.
        """
        super(PosTagVisualizer, self).__init__(ax=ax, **kwargs)

        # TODO: hard-coding in the ANSII colormap for now.
        # Can we let the user reset the colors here?
        self.COLORS = {
            'white'      : "\033[0;37m{}\033[0m",
            'yellow'     : "\033[0;33m{}\033[0m",
            'green'      : "\033[0;32m{}\033[0m",
            'blue'       : "\033[0;34m{}\033[0m",
            'cyan'       : "\033[0;36m{}\033[0m",
            'red'        : "\033[0;31m{}\033[0m",
            'magenta'    : "\033[0;35m{}\033[0m",
            'black'      : "\033[0;30m{}\033[0m",
            'darkwhite'  : "\033[1;37m{}\033[0m",
            'darkyellow' : "\033[1;33m{}\033[0m",
            'darkgreen'  : "\033[1;32m{}\033[0m",
            'darkblue'   : "\033[1;34m{}\033[0m",
            'darkcyan'   : "\033[1;36m{}\033[0m",
            'darkred'    : "\033[1;31m{}\033[0m",
            'darkmagenta': "\033[1;35m{}\033[0m",
            'darkblack'  : "\033[1;30m{}\033[0m",
             None        : "\033[0;0m{}\033[0m"
        }

        self.TAGS = {
            'NN'   : 'green',
            'NNS'  : 'green',
            'NNP'  : 'green',
            'NNPS' : 'green',
            'VB'   : 'blue',
            'VBD'  : 'blue',
            'VBG'  : 'blue',
            'VBN'  : 'blue',
            'VBP'  : 'blue',
            'VBZ'  : 'blue',
            'JJ'   : 'red',
            'JJR'  : 'red',
            'JJS'  : 'red',
            'RB'   : 'cyan',
            'RBR'  : 'cyan',
            'RBS'  : 'cyan',
            'IN'   : 'darkwhite',
            'POS'  : 'darkyellow',
            'PRP$' : 'magenta',
            'PRP$' : 'magenta',
            'DT'   : 'black',
            'CC'   : 'black',
            'CD'   : 'black',
            'WDT'  : 'black',
            'WP'   : 'black',
            'WP$'  : 'black',
            'WRB'  : 'black',
            'EX'   : 'yellow',
            'FW'   : 'yellow',
            'LS'   : 'yellow',
            'MD'   : 'yellow',
            'PDT'  : 'yellow',
            'RP'   : 'yellow',
            'SYM'  : 'yellow',
            'TO'   : 'yellow',
            'None' : 'off'
        }

    def colorize(self, token, color):
        """
        Colorize text

        Parameters
        ----------
        token : str
            A str representation of

        """
        return self.COLORS[color].format(token)

    def transform(self, tagged_tuples):
        """
        The transform method transforms the raw text input for the
        part-of-speech tagging visualization. It requires that
        documents be in the form of (tag, token) tuples.

        Parameters
        ----------
        tagged_token_tuples : list of tuples
            A list of (tag, token) tuples

        Text documents must be tokenized and tagged before passing to fit()
        """
        self.tagged = [
            (self.TAGS.get(tag),tok) for tok, tag in tagged_tuples
        ]

        print(' '.join((self.colorize(token, color) for color, token in self.tagged)))
        print('\n')

```

## Conclusion
So, this works pretty well in the console. It also works in a _live_ Jupyter Notebook, however I noticed that when I saved it as an [.ipynb file](https://github.com/DistrictDataLabs/yellowbrick/blob/develop/examples/rebeccabilbro/postag.ipynb) and pushed to GitHub, it converted all the text to black and I lost the colorization.
