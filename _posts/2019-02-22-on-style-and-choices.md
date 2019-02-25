---
layout: post
title:  On Style and Choices - PEP8 and Beyond
image:
  feature: pepper_crop.png
tags:   programming
date:   2019-02-22 10:54
---

Recently I joined a new team, which consists of a mixture of Python and Clojure programmers. While this has caused me to spend a little time thinking about [Clojure and it's application to the kind of work I do](https://www.amazon.com/Clojure-Data-Science-Henry-Garner/dp/1784397180), I'm still mainly using Python. Python (and all the 3rd party libraries available via [PyPI](https://pypi.org/)) make it a particularly good tool for building NLP, video processing, and machine learning prototypes and microservices in the service of my company's larger application. But, even though I'm primarily writing Python and reviewing code from data scientists who write in Python, the position change has definitely required some time for mutual acclimation!

## Write and Wrong: Lessons from The Writing Center

I believe that writing, whether you're writing prose, poetry, or code, is fundamentally a creative act. One thing I always think about when working with a new team is the importance of acclimating to other team members' writing styles, and learning to respect and appreciate their creative choices. 

A long time ago, when I was in college, I had a job working at the [Writing Center](https://www.skidmore.edu/writingcenter/). The Writing Center held regular hours during which time other students, faculty, and staff could drop by to get help with things they were writing &mdash; essays, resumes, theses, even book manuscripts. It paid ok, and I was a lot better at it than I had been at making sandwiches (my previous gig), so I ended up continuing the job into graduate school. 

One of the most valuable things I learned from my years working at the Writing Center is that while there are some "rules" about writing that are more or less hard and fast (though, honestly, these too are debatable, contextual, and always evolving), most of the way we choose to write is just that &mdash; a *choice*.

When people come to the Writing Center to have their writing reviewed, it's tempting to change everything to the way you would write it. But just because you write differently from me doesn't mean that one of us is writing the correct way, and the other way is wrong. In a surprising number of cases, there isn't a clearly defined **correct way**.


## Rules, Algorithms, Conventions

To be sure, with code there are certain **syntactic rules** that define how programs will be written/compiled/interpreted. These include things like [*reserved words*](https://docs.python.org/3.3/reference/lexical_analysis.html#keywords) that can't be used as ordinary identifiers, *control flow* markers like braces, keywords, and whitespace to delimit blocks of code, *data types*, *operators* that specify the kinds of arithmatic, comparative, and logical operations that are legal in that language, and other language-specific provisions, like [*concurrency*](https://www.golang-book.com/books/intro/10), [*polymorphism*](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)), or [*macros*](http://www.paulgraham.com/avg.html). 

There are also [**algorithms**](https://en.wikipedia.org/wiki/List_of_algorithms) that help inform the efficiency, practicality, scalability, safety, and speed of our code. 

Then there are **"cultural" conventions**, such as *case* (e.g. snakecase, camelcase, etc.), *indentation* (i.e. spaces vs. tabs), *closing delimiters* (e.g. trailing commas, semicolons, etc) and *line length*. These are conventions that are adopted by the community, and which we tend to adopt to optimize for mutual comprehension; these aren't things we do so that the code will run, or so that it will run quickly, but so that other programmers will be able to more easily read, understand, maintain, and modify our code. For Python, these conventions are laid out in the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/).

## Styles and Preferences

In the interest of facilitating a discussion with my team about Pythonic conventions and personal stylistic choices, and with an eye toward developing a shared team style, I asked my teammates to reread or read (we have some brand-new programmers) PEP 8 and consider a few questions:

1. "A Python style question I always wondered about was `{ }`  according to the PEP 8 guide, the convention is `{ }`"
2. "One thing I never knew about Python style that I learned from PEP 8 was `{ }`"
3. "One question the PEP 8 guide didn't answer for me was what to do about `{ }`"
4. "One thing that PEP 8 says that I disagree with is `{ }` because `{ }`."

For now, I'll just record my own responses, though later I'll try to come back and integrate some additional thoughts and reactions from the team.

### I Really (Like, Irrationally) Like...
... staying at or under the maximum character length (code lines: 79 chars, docstring lines: 72 chars). This is one of the conventions that I really notice in other people's code. Side-to-side scrolling is super annoying, and this is something that bothers me when I read code written in Go, where there is no line length convention. In my own coding, I install a linter plugin to my IDE or editor so that I'll be alerted to any violations of this rule as I'm writing or reviewing code.

On the other hand, I really hate using backslashes for line breaks. This just looks clunky to me:

```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

I'd almost certainly do something like this to avoid getting into the above situation:

```python
READ_PATH = '/path/to/some/file/you/want/to/read'
WRITE_PATH = '/path/to/some/file/being/written'

with open(READ_PATH) as file_1, open(WRITE_PATH, 'w') as file_2:
    file_2.write(file_1.read())
```

The rule of thumb I like to use is [Trey Hunner's, that line length is about readability, not length](https://youtu.be/knMg6G9_XCg?t=201).

### I'm Still Not Always Sure...
...where to break lines. In particular, I've recently encountered a lot of code that had very complex if/else control flows that depended on many conditions. In the example from PEP8, I think my preference is for this style: 

```python
if (this_is_one_thing
        and that_is_another_thing
        and yet_another_thing
        and one_last_thing):
    do_something()
```

For multiline closing parens, braces, and brackets, my preference is for:

```python
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)

my_dict = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
}

my_list = [
    1, 2, 3,
    4, 5, 6,
]

```

With docstrings, I prefer:

```python

class WorkerBee(Bee):
    """
    A WorkerBee is a kind of bee, whose job it is to make honey,
    protect the queen and hive, but not to lay eggs or mate.
    """
    ...

```
But with multiline strings, we have to be a little careful about injecting newlines:

```python

poem = """
Whose woods these are I think I know.   
His house is in the village though;   
He will not see me stopping here   
To watch his woods fill up with snow.   

My little horse must think it queer   
To stop without a farmhouse near   
Between the woods and frozen lake   
The darkest evening of the year.   

He gives his harness bells a shake   
To ask if there is some mistake.   
The only other sound’s the sweep   
Of easy wind and downy flake.   

The woods are lovely, dark and deep,   
But I have promises to keep,   
And miles to go before I sleep,   
And miles to go before I sleep.
"""

```

When in doubt, or when I have to break a really weird line, I'll sometimes add extra parenthesis to allow for implicit line continuations.

```python
s = ("Area: {0}, Estimated ({1}): {2}"
    .format(area, points, estimate(radius, points))
    )

print(
    ("""And miles to go before I sleep, """
     """And miles to go before I sleep.""")
)   
```

### One Thing that Stood Out to Me on This Read...

Boolean comparisons:
 - empty strings, lists, and tuples evaluate to `False` (perhaps I noticed it this time since I've been working in Go, which has [zero values](https://tour.golang.org/basics/12))
 - comparing boolean values to `True` or `False` using `==` or `!=` or `is` is a no-no!

### I Never Fully Absorbed...

...how to use blank lines. Even though I've read through PEP 8 several times now over the years, I don't think I ever really absorbed the guidance on blank lines before now. Summary:

**ONE BLANK LINE** 
 - before and after method definitions
 - separating standard lib from third party from local imports

**TWO BLANK LINES** 
 - after import statements
 - before and after class definitions
 - between each function (outside of classes)

### Personal Preferences...

Note that all of PEP 8 still leaves a surprising amount of detail open to choice! Here are some of my own personal preferences

#### Imports
Some people list imports alphabetically, other people just do it randomly. I really, really like to organize imports so that they taper, either up or down (I don't really care):

```python

import os
import sys
import json

from sklearn.svc import SVM
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression

from beehive import QueenBee
from beehive import WorkerBee
```

#### Extra Whitespace for Alignment

I also like to add extra whitespaces to make things like statements and dictionary entries line up:

```python

# This is how you're supposed to do it
not_lined_up = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
}

# I like this better
lined_up = {
    "one"   : 1,
    "two"   : 2,
    "three" : 3,
}


# This is how you're supposed to do it
a = b + c
two = 1 + 1
dogs = "man's best friend"

# I like this better
a    = b + c
two  = 1 + 1
dogs = "man's best friend"
```

#### Naming Things

The PEP8 guidance on module and function names is that they should have short, all-lowercase names, and that underscores are to be avoided. I really don't care for using underscores in names in general; they look clunky to me and make lines longer. 

I like class names to sound like they would make sense as the subject of a sentence (e.g. "The `QueenBee` is in charge of making more bees.") 

For variable names, I like them to be descriptive and distinct but also short and with as few underscores as possible (e.g. instead of `df` or `test_df` or `scores_df_with_bad_vals_dropped`, something like `scores` or `test_scores` or `clean_scores`). This is also helpful for maintaining shorter line lengths!

This also goes for function names, which I think of as being mainly just conjugations of verbs (e.g. just `writer` rather than `file_writer` unless you also have `db_writer`. Definitely not `csv_file_writer` unless you also have `excel_file_writer` &mdash; but in this case I'd probably just re-write the function to take a filetype parameter, e.g. `def writer(ftype)`). 

## Further Reading/Watching

One of the best ways to learn Pythonic conventions *and* develop a personal style is to read other people's code! Here are some resources I like:

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 526 - Variable Annotations](https://www.python.org/dev/peps/pep-0526/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Trey Hunner - Readability Counts (video)](https://youtu.be/knMg6G9_XCg)
- [Trey Hunner - Craft Your Python Like Poetry](https://treyhunner.com/2017/07/craft-your-python-like-poetry/)
- [Jacob Burch - The Other Hard Problem: Lessons and Advice on Naming Things (video)](https://youtu.be/bg1wdbKBRKg)
- [Raymond Hettinger - Beyond PEP 8: Best practices for beautiful intelligible code (video)](https://youtu.be/wf-BqAjZb8M)
- [Lacey Williams Henschel - Jane Austen on PEP8: Tips from an English Major on Writing Better Code](https://youtu.be/55gXwFviOuQ)
