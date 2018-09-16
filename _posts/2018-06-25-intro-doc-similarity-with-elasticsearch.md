---
layout: post
title:  Introduction to Document Similarity with Elasticsearch
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-06-25 15:42
---

In a text analytics context, document similarity relies on reimagining texts as points in space that can be close (similar) or different (far apart). However, it's not always a straightforward process to determine which document features should be encoded into a similarity measure (words/phrases? document length/structure?). Moreover, in practice it can be challenging to find a quick, efficient way of finding similar documents given some input document. In this post I'll explore some of the similarity tools implemented in Elasticsearch, which can enable us to augment search speed without having to sacrifice too much in the way of nuance.

## Document Distance and Similarity

In this post I'll be focusing mostly on getting started with Elasticsearch and comparing the built-in similarity measures currently implemented in ES. However, if you're new to the concept of document similarity, here's a quick overview.

Essentially, to represent the distance between documents, we need two things: first, a way of encoding text as vectors, and second, a way of measuring distance.

 1. The bag-of-words (BOW) model enables us to represent document similarity with respect to vocabulary and is easy to do. Some common options for BOW encoding include one-hot encoding, frequency encoding, TF-IDF, and distributed representations.
 2. How should we measure distance between documents in space? Euclidean distance is often where we start, but is not always the best choice for text. Documents encoded as vectors are sparse; each vector could be as long as the number of unique words across the full corpus.  That means that two documents of very different lengths (e.g. a single recipe and a cookbook), could be encoded with the same length vector, which might overemphasize the magnitude of the book's document vector at the expense of the recipe's document vector. Cosine distance helps to correct for variations in vector magnitudes resulting from uneven length documents, and enables us to measure the distance between the book and recipe.

For more about vector encoding, you can check out Chapter 4 of [our book](https://www.amazon.com/Applied-Text-Analysis-Python-Language-Aware/dp/1491963042), and for more about different distance metrics check out Chapter 6. In Chapter 10, we prototype a kitchen chatbot that, among other things, uses a [nearest neigbor](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) search to recommend recipes that are similar to the ingredients listed by the user. You can also poke around in the code for the book [here](https://github.com/foxbook/atap).

One of my observations during the prototyping phase for that chapter is how slow vanilla nearest neighbor search is. This led me to think about different ways to optimize the search, from using variations like [ball tree](https://en.wikipedia.org/wiki/Ball_tree), to using other Python libraries like [Spotify's Annoy](https://github.com/spotify/annoy), and also to other kind of tools altogether that attempt to deliver a similar results as quickly as possible.

I tend to come at new text analytics problems non-deterministically (e.g. a __machine learning perspective__), where the assumption is that similarity is something that will (at least in part) be _learned_ through the training process. However, this assumption often requires a not insignificant amount of data to begin with to support that training. In an application context where little training data may be available to begin with, Elasticsearch's similarity algorithms (e.g. an __engineering approach__)seem like a potentially valuable alternative.

## What is Elasticsearch
[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html) is a open source text search engine that leverages the information retrieval library Lucene together with a key-value store to expose deep and rapid search functionalities. It combines the features of a NoSQL document store database, an analytics engine, and RESTful API, and is particularly useful for indexing and searching text documents.

### The Basics
To run Elasticsearch, you need to have the Java JVM (>= 8) installed. For more on this, read the [installation instructions](https://www.elastic.co/guide/en/elasticsearch/reference/master/setup.html).

In this section, we'll go over the basics of starting up a local elasticsearch instance, creating a new index, querying for all the existing indices, and deleting a given index. If you know how to do this, feel free to skip to the next section!

#### Start Elasticsearch
In the command line, start running an instance by navigating to where ever you have elasticsearch installed and typing:

```bash
$ cd elasticsearch-<version>        
$ ./bin/elasticsearch
```

#### Create an Index
Now we will create an index. Think of an index as a database in PostgreSQL or MongoDB. An Elasticsearch cluster can contain multiple indices (e.g. relational or noSql databases), which in turn contain multiple types (similar to MongoDB collections or PostgreSQL tables). These types hold multiple documents (similar to MongoDB documents or PostgreSQL rows), and each document has properties (like MongoDB document key-values or PostgreSQL columns).

```bash
curl -X PUT "localhost:9200/cooking " -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 1
        }
    }
}
'
```

 And the response:

```bash
{"acknowledged":true,"shards_acknowledged":true,"index":"cooking"}
```

#### Get All Indices

```bash
$ curl -X GET "localhost:9200/_cat/indices?v"
```

#### Delete a Specific Index

```bash
$ curl -X DELETE "localhost:9200/cooking"
```

### Document Relevance

To explore how Elasticsearch approaches document relevance, let's begin by manually adding some documents to the cooking index we created above:

```bash
$ curl -X PUT "localhost:9200/cooking/_doc/1?pretty" -H 'Content-Type: application/json' -d'
{
      "description":  "Smoothies are one of our favorite breakfast options year-round."
}
'
```

```bash
$ curl -X PUT "localhost:9200/cooking/_doc/2?pretty" -H 'Content-Type: application/json' -d'
{
      "description":  "A smoothie is a thick, cold beverage made from pureed raw fruit."
}
'
```

```bash
$ curl -X PUT "localhost:9200/cooking/_doc/3?pretty" -H 'Content-Type: application/json' -d'
{
      "description":  "Eggs Benedict is a traditional American breakfast or brunch dish."
}
'
```    

At a very basic level, we can think of Elasticsearch's basic search functionality as a kind of similarity search, where we are essentially comparing the bag-of-words formed by the search query with that of each of our documents. This allows Elasticsearch not only to return results that explicitly mention the desired search terms, but also to surface a score that conveys some measure of relevance.

We now have three breakfast-related documents in our cooking index; let's use the basic search function to find documents that explicitly mention "breakfast":

```bash
$ curl -XGET 'localhost:9200/cooking/_search?q=description:breakfast&pretty'
```

And the response:

```bash
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 2,
    "max_score" : 0.48233607,
    "hits" : [
      {
        "_index" : "cooking",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.48233607,
        "_source" : {
          "description" : "Smoothies are one of our favorite breakfast options year-round."
        }
      },
      {
        "_index" : "cooking",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.48233607,
        "_source" : {
          "description" : "Eggs Benedict is a traditional American breakfast or brunch dish."
        }
      }
    ]
  }
}
```

We get two results back, the first and third documents, which each have the same relevance score, because both include the single search term exactly once.

However if we look for documents that mention "smoothie"...

```bash
$ curl -XGET 'localhost:9200/cooking/_search?q=description:smoothie&pretty'
```

...we only get the second document back, since the word "smoothie" is pluralized in the first document. On the other hand, our relevance score has jumped up to nearly 1, since it is the only result in the index that contains the search term.

```bash
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 0.9331132,
    "hits" : [
      {
        "_index" : "cooking",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.9331132,
        "_source" : {
          "description" : "A smoothie is a thick, cold beverage made from pureed raw fruit."
        }
      }
    ]
  }
}
```

We can work around this by using a fuzzy search, which will return both the first and second documents:


```bash
curl -XGET "localhost:9200/cooking/_search?pretty=true" -H 'Content-Type: application/json' -d'
{
    "query": {
       "fuzzy" : { "description" : "smoothie" }
    }
}
'
```

With the following results:

```bash
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 2,
    "max_score" : 0.9331132,
    "hits" : [
      {
        "_index" : "cooking",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.9331132,
        "_source" : {
          "description" : "A smoothie is a thick, cold beverage made from pureed raw fruit."
        }
      },
      {
        "_index" : "cooking",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.8807446,
        "_source" : {
          "description" : "Smoothies are one of our favorite breakfast options year-round."
        }
      }
    ]
  }
}
```

## Searching a Real Corpus

In order to really appreciate the differences and nuances of different similarity measures, we need more than three documents! For convenience, we'll use the sample text corpus that comes with the machine learning visualization library [Yellowbrick](http://www.scikit-yb.org/en/latest/) (which you can install via `pip`).

Yellowbrick hosts several datasets wrangled from the UCI Machine Learning Repository or built by District Data Labs to present the examples used throughout this documentation, one of which is a text corpus of news documents collected from different domain area RSS feeds. If you haven't downloaded the data, you can do so by running:

    $ python -m yellowbrick.download

This should create a folder named data in your current working directory that contains all of the datasets. You can load a specified dataset as follows:

<script src="https://gist.github.com/rebeccabilbro/a9a3143ff0b20a51f17b65de6284890e.js"></script>

The categories in the hobbies corpus include: "cinema", "books", "cooking", "sports", and "gaming". We can explore them like this:

```python
food_stories = [text for text in hobby_types['cooking']]
print(food_stories[5])
```

    Smoothies are one of our favorite breakfast options year-round, but especially in the winter because it's an easy way to brighten the mornings by adding extra fruit to our diets. And since frozen fruit works just as well (if not better — hello, icy, creamy texture), there's no worry about whether it's in season. If you're stuck in the doldrums of gray days, try these tropical smoothies. It won't be quite like you're relaxing on a white-sand beach, but it'll be closer to it than your normal bowl of oatmeal. Sometimes, you just have to go with a classic...

Most of the articles, like the one above, are straightforward and are clearly correctly labeled, though there are some exceptions:

```python
print(food_stories[23])
```

    When Elise and Ben bought their Mount Washington house, the kitchen looked like this. They used this sad kitchen for five years until they finally updated it. The end result is modernized, but still captures the spirit and integrity of the storied older house. Using IKEA cabinets to keep the costs down, they were able to upgrade and personalize the look with Calcutta marble and Schoolhouse Electric hardware for all the cabinets...


## Elasticsearch and Python

We can use the [`elasticsearch` library](https://elasticsearch-py.readthedocs.io/en/master/) in Python (which you can install via `pip`) to hop out of the command line and interact with our Elasticsearch instance a bit more systematically. Here we'll create a class that goes through each of the hobbies categories in the corpus and indexes each to a new index appropriately named after it's category:

<script src="https://gist.github.com/rebeccabilbro/5eae62bd85a8e270309d34e75047320b.js"></script>

```python
indexer = ElasticIndexer()
indexer.index(hobby_types.items())
```

Let's poke around a bit to see what's in our instance. Note: after running the above, you should see the indices appear when you type `curl -X GET "localhost:9200/_cat/indices?v"` into the command line.


```python
from pprint import pprint

query = {"match_all": {}}
result = indexer.elastic_search.search(index="cooking", body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    30 hits

    First result:

    {'_id': 'nNmYOGQB7PzBcXb-nYux',
     '_index': 'cooking',
     '_score': 1.0,
     '_source': {'description': 'Let’s take a moment to admire the ugly celeriac. '
                                'Such an awesome root. Really affordable to buy, '
                                'filled with flavour and so versatile to use. '
                                'Plus, it’s thick, wrinkly, handle cold '
                                'temperatures well and can therefor be harvested '
                                'all through the winter. We had some celeriac left '
                                'in the fridge after we had made this dish and '
                                'used some of those leftovers to make thin and '
                                'crispy celeriac chips and chopped the rest into a '
                                'carrot & celeriac soup that, with a dash of white '
                                'wine, was right on point. But we are not here for '
                                'the leftovers, are we? ...'},
     '_type': '_doc'}

```python
query = {"fuzzy":{"description":"breakfast"}}
result = indexer.elastic_search.search(index="cooking", body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    8 hits

    First result:

    {'_id': 'ntmYOGQB7PzBcXb-nYux',
     '_index': 'cooking',
     '_score': 2.5346222,
     '_source': {'description': 'Take a walk through the freezer section at any '
                                "grocery store and you're likely find almost an "
                                'entire aisle devoted to microwavable meals. From '
                                'rice bowls to mac and cheese to lasagna — the '
                                'options are endless. But even the ones that claim '
                                "to be nutritious or healthful don't beat an "
                                'equally quick meal made at home with the aid of '
                                "the microwave...'},
     '_type': '_doc'}


### More Like This
Elasticsearch exposes a convenient way of doing more advanced querying based on document similarity, which is called "More Like This" ([MLT](https://www.elastic.co/guide/en/elasticsearch/reference/1.6/query-dsl-mlt-query.html)). Given an input document or set of documents, MLT wraps all of the following behavior:

 - extraction of a set of representative terms from the input
 - selection of terms with the highest scores*
 - formation of a disjunctive query using these terms
 - query execution
 - results returned

*_Note: this is done using term frequency-inverse document frequency (TF-IDF). Term frequency-inverse document frequency is an encoding method that normalizes term frequency in a document with respect to the rest of the corpus. As such, TF-IDF measures the relevance of a term to a document by the scaled frequency of the appearance of the term in the document, normalized by the inverse of the scaled frequency of the term in the entire corpus. This has the effect of selecting terms that make the input document or documents the most unique._

We can now build an MLT query in much the same way as we did the `"fuzzy"` search above. The Elasticsearch MLT query exposes many [search parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html#_document_input_parameters), but the only required one is `"like"`, to which we can specify a string, a document, or multiple documents.

Let's see if we can find any documents from our corpus that are similar to a New York Times [review](https://www.nytimes.com/2018/05/29/dining/don-angie-review.html) for the Italian restaurant Don Angie.


```python
red_sauce_renaissance = """
    Ever since Rich Torrisi and Mario Carbone began rehabilitating chicken Parm and
    Neapolitan cookies around 2010, I’ve been waiting for other restaurants to carry
    the torch of Italian-American food boldly into the future. This is a major branch
    of American cuisine, too important for its fate to be left to the Olive Garden.
    For the most part, though, the torch has gone uncarried. I have been told that
    Palizzi Social Club, in Philadelphia, may qualify, but because Palizzi is a
    veritable club — members and guests only, no new applications accepted — I don’t
    expect to eat there before the nation’s tricentennial. Then in October, a place
    opened in the West Village that seemed to hit all the right tropes. It’s called
    Don Angie. Two chefs share the kitchen — Angela Rito and her husband, Scott
    Tacinelli — and they make versions of chicken scarpariello, antipasto salad and
    braciole. The dining room brings back the high-glitz Italian restaurant décor of
    the 1970s and ’80s, the period when Formica and oil paintings of the Bay of Naples
    went out and mirrors with gold pinstripes came in. The floor is a black-and-white
    checkerboard. The bar is made of polished marble the color of beef carpaccio.
    There is a house Chianti, and it comes in a straw-covered bottle. There is hope
    for a red-sauce renaissance, after all.
"""
```


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "min_term_freq" : 3,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index="cooking", body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    25 hits

    First result:

    {'_id': 's9mYOGQB7PzBcXb-nYux',
     '_index': 'cooking',
     '_score': 3.680807,
     '_source': {'description': 'Chopped fans, ever wonder: Who puts together the '
                                'mystery baskets? Where does the fourth plate of '
                                'food go? Does Ted Allen ever get a taste? Do the '
                                'judges really have to eat that? Chopped host Ted '
                                'Allen took the time to sit down with Food Network '
                                'to answer the questions fans have been asking and '
                                'wondering about through the many seasons of the '
                                'show. He reveals some of the secrets behind one '
                                'of the most-popular cooking competition shows on '
                                'TV...'},
     '_type': '_doc'}


#### Unlike

Note that we can also add the `unlike` parameter to limit our search. Here I've indicated some of the less food-related stories that we found while doing exploratory analysis:


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "unlike" : [food_stories[23], food_stories[28]],
        "min_term_freq" : 2,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index="cooking", body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    4 hits

    First result:

    {'_id': 'r9mYOGQB7PzBcXb-nYux',
     '_index': 'cooking',
     '_score': 0.88742733,
     '_source': {'description': 'Rosemary Chicken Salad with Avocado and Bacon 10 '
                                'Smart Points 381 Calories This hearty Rosemary '
                                'Chicken Salad with Avocado and Bacon is HUGE – '
                                'perfect when you want a low-carb meal that will '
                                'fill you up! I actually split this between three '
                                'people, and felt completely satisfied. This '
                                'delicious recipe is from Heather Christo’s first '
                                'cookbook Pure Delicious. A cookbook filled with '
                                '150 Allergen-Free recipes including gluten, '
                                'dairy, soy, nut, shellfish and cane sugar...'},
     '_type': '_doc'}


We can also expand our search to other indices, to see if there are documents related to our red sauce renaissance article that may appear in other hobbies corpus categories:


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "unlike" : [food_stories[23], food_stories[28]],
        "min_term_freq" : 2,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index=["cooking","books","sports"], body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    17 hits

    First result:

    {'_id': 'YtmYOGQB7PzBcXb-nYyy',
     '_index': 'sports',
     '_score': 2.463918,
     '_source': {'description': 'Welshman Jamie Donaldson saw his chances of '
                                'victory at the Houston Open fade after a poor '
                                'third round. The 40-year-old Ryder Cup player was '
                                'three shots off the lead at the halfway stage but '
                                'a 74 leaves him six shots adrift. American pair '
                                'Jim Herman and Jamie Lovemark share the lead on '
                                "11 under. Sweden's Henrik Stenson and Americans "
                                'Dustin Johnson and Russell Henley are a further '
                                'shot behind in the last event before the '
                                'Masters.'},
     '_type': '_doc'}


## Advanced Similarity

So far we've explored how to get started with Elasticsearch and to perform basic search and fuzzy search. These search tools all use the [practical scoring function](https://www.elastic.co/guide/en/elasticsearch/guide/current/practical-scoring-function.html) to compute the relevance score for search results. This scoring function is a variation of TF-IDF that also takes into account a few other things, including the length of the query and the field that's being searched.

Now we will look at some of the more advanced tools implemented in Elasticsearch. Similarity algorithms can be set on a per-index or per-field basis. The available similarity computations include:

 - BM25 similarity (`BM25`): currently the default setting in Elasticsearch, BM25 is a TF-IDF based similarity that has built-in tf normalization and supposedly works better for short fields (like names).
 - Classic similarity (`classic`): TF-IDF
 - Divergence from Randomness (`DFR`): Similarity that implements the divergence from randomness framework.
 - Divergence from Independence (`DFI`): Similarity that implements the divergence from independence model.
 - Information Base Model (`IB`): Algorithm that presumes the content in any symbolic 'distribution' sequence is primarily determined by the repetitive usage of its basic elements.
 - LMDirichlet Model (`LMDirichlet`): Bayesian smoothing using Dirichlet priors.
 - LM Jelinek Mercer (`LMJelinekMercer`): Attempts to capture important patterns in the text but leave out the noise.

### Changing the Default Similarity
If you want to change the default similarity after creating an index you must close your index, send the following request and open it again afterwards:

```bash
curl -X POST "localhost:9200/cooking/_close"
curl -X PUT "localhost:9200/cooking/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "similarity": {
      "default": {
        "type": "classic"
      }
    }
  }
}
'
curl -X POST "localhost:9200/cooking/_open"

```

#### Classic TF-IDF

Now that we've manually changed the similarity scoring metric (in this case to classic TF-IDF), we can see how this effects the results of our previous queries, where we note right away that the first result is the same, but it's relevance score is lower.


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "unlike" : [food_stories[23], food_stories[28]],
        "min_term_freq" : 2,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index=["cooking"], body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    4 hits

    First result:

    {'_id': 'r9mYOGQB7PzBcXb-nYux',
     '_index': 'cooking',
     '_score': 0.19453105,
     '_source': {'description': 'Rosemary Chicken Salad with Avocado and Bacon 10 '
                                'Smart Points 381 Calories This hearty Rosemary '
                                'Chicken Salad with Avocado and Bacon is HUGE – '
                                'perfect when you want a low-carb meal that will '
                                'fill you up! I actually split this between three '
                                'people, and felt completely satisfied. This '
                                'delicious recipe is from Heather Christo’s first '
                                'cookbook Pure Delicious. A cookbook filled with '
                                '150 Allergen-Free recipes including gluten, '
                                'dairy, soy, nut, shellfish and cane sugar...'},
     '_type': '_doc'}


#### LMDirichlet Similarity

...whereas when we change `"type": "LMDirichlet"`, our same document appears with a much higher score:


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "unlike" : [food_stories[23], food_stories[28]],
        "min_term_freq" : 2,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index=["cooking"], body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    4 hits

    First result:

    {'_id': 'L_XaOGQBFKlACkFk94GK',
     '_index': 'cooking',
     '_score': 1.3233942,
     '_source': {'description': 'Rosemary Chicken Salad with Avocado and Bacon 10 '
                                'Smart Points 381 Calories This hearty Rosemary '
                                'Chicken Salad with Avocado and Bacon is HUGE – '
                                'perfect when you want a low-carb meal that will '
                                'fill you up! I actually split this between three '
                                'people, and felt completely satisfied. This '
                                'delicious recipe is from Heather Christo’s first '
                                'cookbook Pure Delicious. A cookbook filled with '
                                '150 Allergen-Free recipes including gluten, '
                                'dairy, soy, nut, shellfish and cane sugar...'},
     '_type': '_doc'}


#### LMJelinekMercer Similarity

...and higher still with `"type": "LMJelinekMercer"`!


```python
query = {
    "more_like_this" : {
        "fields" : ["description"],
        "like" : red_sauce_renaissance,
        "unlike" : [food_stories[23], food_stories[28]],
        "min_term_freq" : 2,
        "max_query_terms" : 50,
        "min_doc_freq" : 4
    }
}

result = indexer.elastic_search.search(index=["cooking"], body={"query":query})

print("%d hits \n" % result['hits']['total'])
print("First result:\n")
pprint(result['hits']['hits'][0])
```

    4 hits

    First result:

    {'_id': 'L_XaOGQBFKlACkFk94GK',
     '_index': 'cooking',
     '_score': 4.9410186,
     '_source': {'description': 'Rosemary Chicken Salad with Avocado and Bacon 10 '
                                'Smart Points 381 Calories This hearty Rosemary '
                                'Chicken Salad with Avocado and Bacon is HUGE – '
                                'perfect when you want a low-carb meal that will '
                                'fill you up! I actually split this between three '
                                'people, and felt completely satisfied. This '
                                'delicious recipe is from Heather Christo’s first '
                                'cookbook Pure Delicious. A cookbook filled with '
                                '150 Allergen-Free recipes including gluten, '
                                'dairy, soy, nut, shellfish and cane sugar...'},
     '_type': '_doc'}


From these simple experiments, we can clearly see that document similarity is not one-size-fits-all, but also that Elasticsearch offers quite a few options for relevance scoring that attempt to take into account the nuances of real-world documents, from variations in length and grammar, to vocabulary and style!  

## TODOs ...

 - custom plugins for Elasticsearch
 - SPARQL + ES
 - Comparing & contrasting results for ES similarity algorithms on large datasets
 - ES sharding & similarity search (in the case of very large datasets)


### Further Reading:

 - [The Practical Scoring Function](https://www.elastic.co/guide/en/elasticsearch/guide/current/practical-scoring-function.html)
 - [How Scoring Works in Elasticsearch](https://www.compose.com/articles/how-scoring-works-in-elasticsearch/)
 - [Elasticsearch Query Efficiency, Part 1](https://compose.com/articles/elasticsearch-query-time-strategies-and-techniques-for-relevance-part-i/)
 - [Elasticsearch Query Efficiency, Part 2](https://compose.com/articles/elasticsearch-query-time-strategies-and-techniques-for-relevance-part-ii/)
 - [Similarity Algorithms Implemented in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html)
 - [How to Change Similarity Algorithm in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/guide/current/changing-similarities.html)
 - [Writing a Custom Similarity Measure for Elasticsearch](http://stefansavev.com/blog/custom-similarity-for-elasticsearch/)
