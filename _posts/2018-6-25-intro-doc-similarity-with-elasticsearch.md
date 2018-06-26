---
layout: post
title:  Introduction to Document Similarity with Elasticsearch
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

In order to really appreciate the differences and nuances of different similarity measures, we need more than three documents! For convenience, we'll use the sample text corpus that comes with the machine learning visualization library [Yellowbrick](http://www.scikit-yb.org/en/latest/). 

Yellowbrick hosts several datasets wrangled from the UCI Machine Learning Repository or built by District Data Labs to present the examples used throughout this documentation, one of which is a text corpus of news documents collected from different domain area RSS feeds. If you haven't downloaded the data, you can do so by running:

    $ python -m yellowbrick.download
    
This should create a folder named data in your current working directory that contains all of the datasets. You can load a specified dataset as follows:


```python
import os

from sklearn.datasets.base import Bunch
from yellowbrick.download import download_all

## The path to the test data sets
FIXTURES  = os.path.join(os.getcwd(), "data")

## Dataset loading mechanisms
datasets = {
    "hobbies": os.path.join(FIXTURES, "hobbies")
}


def load_data(name, download=True):
    """
    Loads and wrangles the passed in text corpus by name.
    If download is specified, this method will download any missing files. 
    """
    
    # Get the path from the datasets 
    path = datasets[name]
    
    # Check if the data exists, otherwise download or raise 
    if not os.path.exists(path):
        if download:
            download_all() 
        else:
            raise ValueError((
                "'{}' dataset has not been downloaded, "
                "use the download.py module to fetch datasets"
            ).format(name))
    
    # Read the directories in the directory as the categories. 
    categories = [
        cat for cat in os.listdir(path) 
        if os.path.isdir(os.path.join(path, cat))
    ]
    
    files  = [] # holds the file names relative to the root 
    data   = [] # holds the text read from the file 
    target = [] # holds the string of the category 
        
    # Load the data from the files in the corpus 
    for cat in categories:
        for name in os.listdir(os.path.join(path, cat)):
            files.append(os.path.join(path, cat, name))
            target.append(cat)
            
            with open(os.path.join(path, cat, name), 'r') as f:
                data.append(f.read())
        
    
    # Return the data bunch for use similar to the newsgroups example
    return Bunch(
        categories=categories,
        files=files,
        data=data,
        target=target,
    )

corpus = load_data('hobbies')
hobby_types  = {}

for category in corpus.categories:
    texts = []
    for idx in range(len(corpus.data)):
        if corpus['target'][idx] == category:
            texts.append(' '.join(corpus.data[idx].split()))
    hobby_types[category] = texts
```

The categories in the hobbies corpus include: "cinema", "books", "cooking", "sports", and "gaming". We can explore them like this:


```python
food_stories = [text for text in hobby_types['cooking']]
print(food_stories[5])
```

    Smoothies are one of our favorite breakfast options year-round, but especially in the winter because it's an easy way to brighten the mornings by adding extra fruit to our diets. And since frozen fruit works just as well (if not better — hello, icy, creamy texture), there's no worry about whether it's in season. If you're stuck in the doldrums of gray days, try these tropical smoothies. It won't be quite like you're relaxing on a white-sand beach, but it'll be closer to it than your normal bowl of oatmeal. Sometimes, you just have to go with a classic. This smoothie recipe is one of our standbys. We might dress it up or down with a touch of mint or swap in coconut water, but we can always count on it to be delicious. You'll definitely get bonus points if you use a fresh coconut to make this smoothie. But because we know mornings are hectic, you can also swap in a can of coconut milk, and it will be just as creamy and delicious. Adding mint to your smoothie is a total pro move. Not only does it amplify the fresh taste, but it also makes it feel slightly more like dessert than a healthy breakfast. This smoothie also has a pinch of sea salt to boost all the other flavors. Don't be fooled by the nondescript hue of this smoothie; it's packed full of tropical flavors including banana, pineapple, mango, and ginger. Plus it gets an added texture from the chia seeds that are mixed in. This rich smoothie is perfect for cooler weather, thanks to the warming spices like cardamom and cinnamon. But before you think it'll taste too much like banana bread, there's a squeeze of lime juice mixed in for a bit of brightness. If you like cilantro, this should be the next smoothie recipe that you try. The subtle spice of the cilantro offsets the sweetness of the pineapple and banana and starts your morning off with an herby kick. Not only does this smoothie get a nutritional boost from fresh (or ground) turmeric, but it also has oats as its base to give it a nice dairy-free creamy consistency. This is the perfect way to use up any of those kiwis that you had the best of intentions of using, but that have been languishing on your counter for just a touch too long. Blend them up with coconut milk, avocado, and some lemon juice (along with water and ice) and you'll end up with a delicious and creamy breakfast. If you have a restricted diet, this is the smoothie template to try. It relies on silken tofu for creaminess, agave syrup for sweetness, and soy milk for smoothness. The only decision you have to make is what kind of fruit to mix in. If you want to make mornings even easier on yourself, try prepping your smoothie ingredients for the week over the weekend and stashing them in the freezer. Then all you have to do is blend and go. Just watch how easy it is: (Image credits: Emily Han; Faith Durand; Chris Perez; Michaela Cisney; Megan Gordon; Sarah Rae Smith; Abe Martinez)


Most of the articles, like the one above, are straightforward and are clearly correctly labeled, though there are some exceptions:


```python
print(food_stories[23])
```

    When Elise and Ben bought their Mount Washington house, the kitchen looked like this. They used this sad kitchen for five years until they finally updated it. The end result is modernized, but still captures the spirit and integrity of the storied older house. Using IKEA cabinets to keep the costs down, they were able to upgrade and personalize the look with Calcutta marble and Schoolhouse Electric hardware for all the cabinets. And what an amazing transformation after: More details to drool over: In Elise's words: I probably made about 12 different floor plans and elevations trying to fit everything in, yet achieve a light, open, airy feeling. The biggest issues were the appliances. How do you fit these huge things, plus a ton of storage space, into a 10x10 room? Really, the only solution was to downsize as much as possible and get a a little creative with the old "kitchen triangle." Breaking up the cooktop and oven, forgoing a good looking oven hood and for a sensible micro hood, and getting the narrowest refrigerator we could find/afford (even if that meant it wasn't counter depth) ended up making the most sense. What we ended up doing: Removed a wall between our tiny kitchen and mud room to make one larger kitchen and create a peninsula for the kids to sit and eat. Removed and replace acoustic ceiling tiles with skim coated drywall Replaced two louvered windows with one awning window IKEA cabinets and fronts in the high gloss white. I looked into both Semi Handmade and Kokeena but because of budget and timing we stuck with IKEA DIY Brass toe kicks Solid Brass hardware Calacutta Marble countertops/backsplash/waterfall White Oak wood floors IKEA refrigerator, microwave and cooktop Smeg oven Elise also has a more DIY tips and details on their kitchen remodel on her blog Burke Decor Blog. She was also gracious enough to share a few valuable lessons she learned during the process of renovating their kitchen using IKEA → Stress-Saving IKEA Kitchen Reno Lessons from a Real Homeowner The surprise that Elise found during renovation was unreal. The house she bought had tenants who lived there for 50 years. It turns out that the previous resident Ruby also wanted new cabinets just as bad as Elise! Thank you Ben and Elise! (Image credits: MLS Listing; Marisa Vitale)


## Elasticsearch and Python

We can use the [`elasticsearch` library](https://elasticsearch-py.readthedocs.io/en/master/) in Python (which you can install via `pip`) to hop out of the command line and interact with our Elasticsearch instance a bit more systematically. Here we'll create a class that goes through each of the hobbies categories in the corpus and indexes each to a new index appropriately named after it's category:


```python
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

class ElasticIndexer(object):
    """
    Create an ElasticSearch instance, and given a list of documents, 
    index the documents into ElasticSearch.
    """
    def __init__(self):
        self.elastic_search = Elasticsearch()
        
    def make_documents(self, textdict):        
        for category, docs in textdict:
            for document in docs:
                yield {
                    "_index": category,
                    "_type": "_doc",
                    "description": document
                }        
    def index(self, textdict):
        bulk(self.elastic_search, self.make_documents(textdict))
        
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
                                'the leftovers, are we? We are here because of '
                                'this little vegan lasagna made on thinly shaved '
                                'celeriac and parsnip “noodles” that are layered '
                                'with a tomato & lentil sauce, mushrooms and '
                                'spinach and then covered with cherry tomatoes and '
                                'baked until soft. For a long time we refused to '
                                'call it lasagna, as we know that people can be a '
                                'little cranky with words. The recipe is made '
                                'entirely without lasagna noodles and béchamel '
                                'sauce which probably is what technically makes a '
                                'lasagna. But in the end we just thought lasagna '
                                'sounded more appealing than casserole and it also '
                                'gives a more visual description of how this dish '
                                'is layered. Our little gif animation further down '
                                'in this post, also helps with that. Regardless of '
                                'its name, this is damn tasty and perfect winter '
                                'food. The roots don’t soak up liquid like lasagna '
                                'so it stays juicy without the need to add a '
                                'creamy sauce. However, if you feel like throwing '
                                'some dairy into it, we can recommend whisking a '
                                'good ricotta with some lemon juice and spreading '
                                'it out as an extra layer in the middle. Replacing '
                                'lasagna noodles with thinly sliced celeriac is a '
                                'great little trick that unfortunately was not '
                                'invented by us. There are a bunch of recipes out '
                                'there, from Gordon Ramsey’s double cream version '
                                'to Sarah Britton’s with butternut squash. On '
                                'another note, yesterday we put a major deadline '
                                'behind us (which is why we have been so slow with '
                                'new blog recipes). It feels great and we will '
                                'tell you all about that project soon. Now we are '
                                'actually off to Asia to sip coconuts, sleep for a '
                                'hundred years and hug or kids, but we have '
                                'prepared a whole array of Christmas recipes that '
                                'we will post next week. And a really beautiful '
                                'and tasty breakfast that we’ll post after '
                                'Christmas – just when you are looking for '
                                'something fresh again. So check back soon! '
                                'Celeriac Lasagna AKA Shaved Roots & Mushroom '
                                'Casserole Serves 6-8 Tomato & Lentil Sauce 1 tbsp '
                                'coconut oil, butter, ghee or olive oil 1 onion 3 '
                                'garlic cloves 1/4 tsp chili flakes 4 cans (6 cups '
                                '/ 1560 g) chopped tomatoes 1/2 cup (125 ml) puy '
                                'lentils (or lentils of choice), rinsed 1 cup (250 '
                                'ml) water 2 sprigs thyme, chopped 20 leaves '
                                'basil, chopped sea salt and pepper Shaved roots 1 '
                                'small celeriac root 3 parsnip roots 1 tbsp '
                                'coconut oil, butter, ghee or olive oil 2 clove '
                                'garlic 20 brown mushrooms 250 g frozen spinach, '
                                'thawed (fresh is fine too) 20 cherry tomatoes (or '
                                '4 regular tomatoes), sliced Preheat the oven to '
                                '350°F / 175°C. Preparing the tomato & lentil '
                                'sauce: Heat oil in a large saucepan. Add onion, '
                                'garlic and chili flakes and sauté for a couple of '
                                'minutes. Add the rest of the ingredients and stir '
                                'to combine. Cover with a lid and let simmer for '
                                'about 45 minutes, until the lentils are soft and '
                                'the sauce is quite ‘dry’. Preparing the celeriac '
                                'and parsnip lasagna noodles: Rinse the roots '
                                'well, then peel, you might want to use a knife '
                                'instead of a peeler. Cut the roots in halves (or '
                                'quarters if it’s large). Slice it in very thin '
                                'slices, best and easiest done with a mandolin '
                                'slicer (3 mm slices). Alternatively use a sharp '
                                'knife, but be careful, and slice as thin as '
                                'possible. Preparing the mushrooms: Clean the '
                                'mushrooms with a soft brush (baking brush or '
                                'toothbrush), if they are very dirty wash them '
                                'with a little water and dry well. Slice the stem '
                                'and the cap lengthwise into large pieces. Heat '
                                'oil and garlic in a skillet on medium-high heat, '
                                'add mushrooms and for a couple of minutes until '
                                'browned on one side, then stir. Fry for a couple '
                                'more minutes and pour into a bowl. Now add the '
                                'thawed spinach to the same skillet with out '
                                'rinsing. When heated, set aside. Assembling the '
                                'lasagna: In an oven proof dish, start with a thin '
                                'layer of oil, cover with a layer of root '
                                '‘noodles’. Add a layer of half of the tomato '
                                'sauce and cover with a layer of root ‘noodles’. '
                                'Add a layer of mushrooms + spinach and a layer of '
                                'root ‘noodles’. Add a layer of the remaining '
                                'tomato sauce and arrange the sliced tomatoes on '
                                'top to cover the tomato sauce. Place the dish in '
                                'the oven and bake for 45-50 minutes. Related'},
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
                                "the microwave. When you're in a pinch or just "
                                'want one less pot or pan to clean, let the '
                                'microwave be the solution for a quick meal you '
                                'make at home, at the office, or in your dorm. 1. '
                                'Think simply. While the microwave can really '
                                'accomplish more kitchen tasks than you might '
                                'think, it really thrives when left to do simple '
                                'jobs, and cooking eggs is one of its best '
                                'examples. Use it to make a quick poached egg, '
                                'which you can place on top of some mixed greens '
                                'for an easy lunch. Or whip up a fast omelet for '
                                'breakfast. Heck, even go and cook up some bacon '
                                "while you're at it. 2. Use quick-cooking "
                                'ingredients. One reason pastas and macaroni and '
                                'cheese bowls are abundant in the microwavable '
                                'meals department is that they are made up of '
                                'ingredients that cook up relatively quickly. '
                                'Whether its dry pasta being cooking for a '
                                'one-bowl serving of mac and cheese, or a '
                                'carefully prepared sauce that makes reheating a '
                                'breeze, pasta is a favorite for meals that are '
                                'made to be microwaved. Read More: How To Make '
                                'One-Bowl Microwave Macaroni and Cheese 3. Lean on '
                                "leftovers. Maybe there's not enough of "
                                "yesterday's chili to just reheat it in the "
                                'microwave and call it dinner, but there just '
                                'might be enough to repurpose it into something '
                                'entirely new with help from your microwave. Use '
                                'it make some hearty baked potatoes or creamy '
                                'polenta, which are the perfect vehicles for '
                                'leftover chili, stew, and even stir-fries, '
                                'turning them into a meal again. 4. Reach for a '
                                'mug. Mugs really are an efficient way to cook in '
                                'the microwave because they hold and distribute '
                                'heat well. If you need to kick a sugar craving '
                                'quickly, a mug cake can be your savior — '
                                "especially when there's Nutella involved. And "
                                'while making French toast or pancakes in a mug '
                                "won't be quite the same as making them the "
                                "traditional way, they're just as satisfying and "
                                'can be made in a whole lot less time. Read More: '
                                '10 Breakfast Recipes You Can Make in a Mug in the '
                                "Microwave 5. Don't forget your vegetables. If you "
                                "haven't tried steaming vegetables in the "
                                'microwave yet, you really should. You can steam '
                                'broccoli or any other vegetable, be it carrots, '
                                'green beans, or cauliflower, using just a '
                                'microwave safe-bowl and plate. After cooking, '
                                'toss them with a little olive oil or butter and '
                                'sprinkle them with salt and pepper and maybe even '
                                'a little grated Parmesan cheese or crumbled feta. '
                                'Add the vegetables to that pasta or polenta you '
                                "made and you've got a light and healthy meal. "
                                'Read More: How to Steam Broccoli in the Microwave '
                                '(Image credits: Emma Christensen)'},
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
                                'TV. Can anyone tell which chef is going to win '
                                'before the cooking begins? Well, like everybody '
                                'else, we kind of pick our favorites as they walk '
                                'in, and just [keep them] in the back of our minds '
                                '… . I got it right on our show that we shot last '
                                'Friday, but you can never really tell, and that’s '
                                'what’s exciting about it. You never can tell, and '
                                'even if someone has the best resume, that doesn’t '
                                'mean that they’re going to get a basket that '
                                'suits them or that’s full of things that they’re '
                                'going to succeed with. What is your favorite '
                                'mystery basket ingredient? Well, out of about '
                                '5,000 of them, that’s going to be sort of hard. I '
                                'mean, gosh, Rocky Mountain oysters, chicken feet '
                                '… we’ve even had eyeballs. My favorite mystery '
                                'basket ingredient remains the whole chicken in a '
                                'can, not so much because I love the food, [but '
                                'because] I love the sound it makes when it plops '
                                'out of the can. Is there a food that freaked you '
                                'out because it was placed in the basket, like '
                                'something out of the ordinary? Yeah. Like, most '
                                'of them. Our baskets can be really, really tough. '
                                'We have had rabbit in a can, chicken in a can, '
                                'chicken feet, all kinds of organs, tongues — many '
                                'different kinds of tongues: duck tongues, cow '
                                'tongues, lamb tongues, pig tongue. We’ve had pig '
                                'lips. Yeah, there have been ingredients that '
                                'freaked me out. Pig nostrils, pig ears, pig '
                                'tails. But here’s the thing: Some things that '
                                'sound weird to you and me as Americans are not '
                                'weird at all in other cultures and other '
                                'countries. We’ve had bugs. We’ve had mealworms. '
                                'We’ve had crickets. We’ve had grasshoppers. We’ve '
                                'had snakes and eels and, you know, foods that are '
                                'totally ordinary — pig blood, mmm, delicious — '
                                'foods that are totally ordinary in other '
                                'countries, and I think that’s part of the '
                                'excitement. We all like [an] ingredient that’s '
                                'going to, you know, make a 12-year-old boy go, '
                                '“Eeew.” Do you ever get to sit down? No, I never '
                                'get to sit down. I’ve asked; they said no. I '
                                'don’t know why they’re obsessed with making me '
                                'stand up all the time. Maybe it’s kind of like '
                                'exercise. Yet people in New York City pay good '
                                'money to exercise, and they have to pay me to do '
                                'it. Is that why you always wear sneakers? I have '
                                'an amazing sneaker collection, thanks to our '
                                'wardrobe stylist, Kitty Boots, and of course '
                                'these sneakers don’t even have laces on them, '
                                'which is kind of handy. I mean, I don’t only wear '
                                'sneakers, but I usually do. It’s because they’re '
                                'comfy, and they’re easy to get in and out of, so '
                                'I do like them for that. … Listen, if you’re a '
                                'cashier or you work in a toll booth and you’re '
                                'standing all day long, it’s good to have comfy '
                                'sneakers, comfy kicks. What happens to the fourth '
                                'plate of food? Does somebody eat it? Why don’t '
                                'you get to taste the food? We send that fourth '
                                'plate directly to my dressing room, where I '
                                'consume it completely every single round. … No, '
                                'nobody eats that. I’ll tell you why. We need the '
                                'fourth plate, because if someone gets Chopped I '
                                'have to have a plate underneath the cloche when I '
                                'lift it, and you don’t want a plate that’s '
                                'already been half-eaten, so that’s the main '
                                'thing. Also, we take close-up shots of that '
                                'fourth plate. By the time we’re done with that '
                                'fourth plate, it’s about two and a half hours '
                                'after it was cooked, and it’s been sitting out at '
                                'room temperature, so no one’s going to eat that. '
                                'That wouldn’t be a good idea. Why do you all '
                                'loathe truffle oil? First of all, truffle oil, '
                                'there’s a time and a place for most ingredients. '
                                '… There are different qualities of truffle oils. '
                                'Some of it is great, some of it’s made with '
                                'artificial ingredients, so that’s one reason. The '
                                'second reason is that it became a fad among '
                                'restaurant chefs to drizzle truffle oil on '
                                'everything, and so when you’re a creative chef, '
                                'the way our judges are, you don’t want to be '
                                'piling onto the bandwagon that everybody else is '
                                'already on. … Three, it’s a very strong '
                                'ingredient and can overwhelm everything else, and '
                                'so combine the fact that we’re a little tired of '
                                'it, [and] if you use too much of it, it can '
                                'really overwhelm a dish. And, finally, it just '
                                'feels like a crutch. Like, people think, “Oh, if '
                                'I put gold leaf and truffle oil and caviar and '
                                'all this expensive, fancy stuff on a dish, that’s '
                                'enough to make it a good dish.” Not really. How '
                                'about just good cooking? Where does the show get '
                                'the leftover ingredients when there’s a leftovers '
                                'battle? This is something that we could all '
                                'relate to. Go to the fridge and there’s nothing '
                                'in there except cold pizza and, you know, a '
                                'leftover soda that you didn’t finish. We get '
                                'those ingredients from totally normal restaurants '
                                'right here in the Chelsea neighborhood. There’s a '
                                'pizza joint up the street that makes really nice '
                                'New York City-style … thin-crust pizza. I '
                                'remember once a guy put a slice of pizza in the '
                                'blender and made a sauce out of it, and it was '
                                'actually good. Why doesn’t the show have a second '
                                'ice cream machine? Everybody’s always fighting '
                                'for the ice cream machine in the dessert round. '
                                'Well, if it were up to me and the judges, we’d '
                                'have 20 ice cream machines and make it easier on '
                                'our contestants. Here’s the dirty little secret: '
                                'Producers of competition shows don’t want to make '
                                'it easy for contestants, so they enjoy it when '
                                'people fight over the ice cream machine. But the '
                                'fact is, it is totally possible for two batches '
                                'of ice cream to get made within a 30-minute '
                                'round, and when that happens, it’s exciting for '
                                'us. So, I don’t think we’re going to add another '
                                'ice cream machine. Who is the most-forgiving '
                                'judge, and who is the least-forgiving judge? '
                                'That’s kind of like the question people ask me, '
                                '“Who’s my favorite judge?” They’re all my '
                                'favorite, and that’s like, you know, when someone '
                                'asks “Who’s your favorite kid?” or “who’s your '
                                'favorite pet?” Our judges are all brilliant in '
                                'totally different ways. Alex Guarnaschelli has, I '
                                'would say, the best gift of language of any of '
                                'our chefs. She can talk, talk, talk and talk so '
                                'beautifully about food like no one I’ve ever '
                                'heard. Scott Conant has this seriousness … '
                                'particularly about foods that matter a lot to '
                                'him, like pasta. Chris Santos has a similar '
                                'seriousness, always passionate, always deeply '
                                'concerned about the cooking. Marcus Samuelsson '
                                'brings such an international worldview. Everybody '
                                'has a different skill set, and I think it’s great '
                                'that they rotate so that we have different people '
                                'there each time. I would say none of them is '
                                'especially forgiving when bad cooking happens, '
                                'but I think they all care deeply about cooking, '
                                'and they care about people. So, they were all '
                                'well-chosen, and I love them all. Do the judges '
                                'have a say in the basket ingredients? After all, '
                                'they do have to eat them. The basket ingredients '
                                'are chosen by a committee that’s led by our '
                                'staffer Sara Hormi, and Sara’s job is to find us '
                                'things that we’ve never seen before, which with '
                                'chefs as great as our judges is a hard thing to '
                                'do. Once in a while, the judges or myself will '
                                'look at a basket and say, “This is just too mean '
                                'or just too hard,” and we’ll ask if something can '
                                'be switched out, and usually they’ll do that for '
                                'us if our concerns are legit, but there’s a lot '
                                'of thought process that goes into choosing those '
                                'ingredients, and by the way, they’re not chosen '
                                'randomly. They’re designed to be possible but '
                                'difficult. … So if we give you, say, tomatillos, '
                                'flatbreads and silky tofu, obviously we’re '
                                'looking for a play on grilled cheese and tomato '
                                'soup, right? The funny thing is the chefs don’t '
                                'have a lot of time to think about it. In fact, '
                                'they have no time to think about it, and they '
                                'really don’t know what the ingredients are, so '
                                'they don’t usually figure out what the riddle is '
                                'inside the basket, but there definitely is an '
                                'intention. Have any of the judges ever gotten '
                                'sick from the food they had to taste? No. I have '
                                'to say after about 5,000 mystery basket '
                                'ingredients the judges have never gotten sick, '
                                'knock on wood, from eating the food, and that’s '
                                'because our culinary department is very serious '
                                'about food safety, and that’s part of their job … '
                                '. Just like when you go to a restaurant, you want '
                                'to have confidence that the food is going to be '
                                'safe. Have any of the judges ever gagged at the '
                                'idea of eating something? There’s a melon that '
                                'comes from Asia called durian that is very '
                                'smelly, and some people love it and a lot of '
                                'people don’t. I remember once we had that in a '
                                'basket, and Geoffrey Zakarian really didn’t want '
                                'to take a bite of that durian. The producers kind '
                                'of made him take one, and I thought he might get '
                                'sick. He also objected to the idea of tasting an '
                                'eyeball, and so would I. So, whenever people say, '
                                '“Why don’t you get to taste the food?’ I always '
                                'say, “How bad do you think I want to taste '
                                'eyeballs, chicken feet and Rocky Mountain '
                                'oysters?” What characteristic is most prevalent '
                                'among Chopped winners? So, I’ve always wanted to '
                                'sit down and write a guide on how to win Chopped '
                                'or how not to lose it, and there are so many '
                                'things you could try to do. I think practicing is '
                                'a great idea — I think especially practicing what '
                                'can you accomplish in 20 minutes, because 20 '
                                'minutes flies by, 30 minutes flies by. I think '
                                'the most-important thing you could do is try to '
                                'cook a bunch of different things within a very '
                                'strict time frame, and don’t give yourself an '
                                'extra minute, because we’re not going to. I think '
                                'winners on Chopped are people who are very '
                                'open-minded and who are quick at getting an idea '
                                'and sticking to it, but also who are quick to go '
                                'to plan B or plan C or plan D, E, F, G, H, I, J, '
                                'K, L, M, N, O — I’m trying to see how much of the '
                                'alphabet I can remember. You have to be able to '
                                'adjust and regroup very quickly, so I would say '
                                '[those are] the top things: Be open-minded, be '
                                'able to come up with an idea very quickly, '
                                'understand what you can cook inside of 20 or 30 '
                                'minutes and be ready to change your plan if '
                                'something goes terribly wrong, because chances '
                                'are it will. How long is the judging time, on '
                                'average? Well, our judges care very deeply about '
                                'fairness. They base their decision entirely on '
                                'the food that’s on the plate. The judges make all '
                                'of the decisions — nobody tells them what to do, '
                                'nobody could. Imagine telling Alex Guarnaschelli '
                                'what to do. Good luck with that. Judging takes '
                                'probably about 15 minutes per round, 15, 20 '
                                'minutes, and we film it, but you only see little '
                                'moments of it. Sometimes there has been [an] '
                                'argument about who should win, which is why we '
                                'have three judges instead of two or four. So, '
                                'there can’t be a tie, and those arguments have '
                                'gone on for 30 or 45 minutes, but usually it’s … '
                                'often very close … . I have to say it’s actually '
                                'really hard. It’s not just, “Well, he won round 1 '
                                'and she won round 2 and then she won round 3, so '
                                'she wins.” It’s not that simple. … We break it '
                                'down: Who used each ingredient in each round the '
                                'best? Who left a mystery basket ingredient off '
                                'the plate? If someone left an ingredient off the '
                                'plate, did somebody else do something even worse? '
                                'It’s actually really complicated. So sometimes it '
                                'takes a while, but … we have to make sure that '
                                'the right person wins. Watch Chopped on Tuesdays '
                                'at 10|9c to see who beats the mystery baskets.'},
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
                                'dairy, soy, nut, shellfish and cane sugar. But '
                                'don’t be fooled, the recipes are amazing and her '
                                'photography is stunning! For this recipe, I '
                                'modified the ingredients slightly to lower the '
                                'calories buy reducing the olive oil a bit, and '
                                'using skinless thighs instead of using the skin. '
                                'If you want to further reduce the calories you '
                                'can use chicken breast instead and use 1/2 of an '
                                'avocado. This recipe was a keeper, also great for '
                                'the summer if you want to make the chicken on the '
                                'grill. Rosemary Chicken Salad with Avocado and '
                                'Bacon This hearty Rosemary Chicken Salad with '
                                'Avocado and Bacon is HUGE – perfect when you want '
                                "a low-carb meal that will fill you up! It's also "
                                'gluten-free, dairy-free, egg-free and soy-free '
                                'for people with food allergies. Ingredients: 3 '
                                'slices center-cut bacon, diced 2 boneless, '
                                'trimmed skinless chicken thighs (4 oz each) 1/2 '
                                'teaspoon kosher salt 1 tbsp fresh rosemary 3 cups '
                                'chopped romaine lettuce, chopped 1/2 cup baby '
                                'arugula or watercress 1/2 cup halved cherry '
                                'tomatoes 3 tablespoons chopped red onion 4 oz '
                                'avocado, sliced (1 small) For the rosemary '
                                'vinaigrette: 1 tsp dijon mustard 4 tsp olive oil '
                                '2 tbsp red wine vinegar 1/2 tsp fresh minced '
                                'rosemary 1/4 teaspoon kosher salt Directions: '
                                'Cook bacon in a large heavy nonstick skillet '
                                'until crispy, about 7 minutes. Transfer to a '
                                'paper towel to drain and set aside. Drain the fat '
                                'but don’t wipe the skillet, leaving any excess '
                                'oil in the pan to cook the chicken. Season '
                                'chicken with salt and rosemary, cook in the '
                                'skillet over medium-high heat until golden and '
                                'cooked through, about 5 minutes on each side. '
                                'Make a bed of the romaine and arugula (or '
                                'watercress) in a large serving bowl or platter '
                                '(or divide between 2 plates). Scatter the cherry '
                                'tomatoes, red onion and bacon on top. Slice the '
                                'avocado, sprinkle with pinch of salt and arrange '
                                'on salad. Slice the chicken thighs and add to the '
                                'salad. To make the rosemary vinaigrette, in a '
                                'small bowl whisk the ingredients. Pour over the '
                                'salad and serve right away. Nutrition Information '
                                'Yield: 2 servings, Serving Size: half of the '
                                'salad Amount Per Serving: Smart Points: 10 Points '
                                '+: 10 Calories: 381 Total Fat: 25g Saturated Fat: '
                                '5g Cholesterol: 114mg Sodium: 741mg '
                                'Carbohydrates: 12g Fiber: 6g Sugar: 1g Protein: '
                                '29g posted April 28, 2016 by Gina Get new free '
                                'recipes and exclusive content delivered right to '
                                'your inbox:'},
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
                                'dairy, soy, nut, shellfish and cane sugar. But '
                                'don’t be fooled, the recipes are amazing and her '
                                'photography is stunning! For this recipe, I '
                                'modified the ingredients slightly to lower the '
                                'calories buy reducing the olive oil a bit, and '
                                'using skinless thighs instead of using the skin. '
                                'If you want to further reduce the calories you '
                                'can use chicken breast instead and use 1/2 of an '
                                'avocado. This recipe was a keeper, also great for '
                                'the summer if you want to make the chicken on the '
                                'grill. Rosemary Chicken Salad with Avocado and '
                                'Bacon This hearty Rosemary Chicken Salad with '
                                'Avocado and Bacon is HUGE – perfect when you want '
                                "a low-carb meal that will fill you up! It's also "
                                'gluten-free, dairy-free, egg-free and soy-free '
                                'for people with food allergies. Ingredients: 3 '
                                'slices center-cut bacon, diced 2 boneless, '
                                'trimmed skinless chicken thighs (4 oz each) 1/2 '
                                'teaspoon kosher salt 1 tbsp fresh rosemary 3 cups '
                                'chopped romaine lettuce, chopped 1/2 cup baby '
                                'arugula or watercress 1/2 cup halved cherry '
                                'tomatoes 3 tablespoons chopped red onion 4 oz '
                                'avocado, sliced (1 small) For the rosemary '
                                'vinaigrette: 1 tsp dijon mustard 4 tsp olive oil '
                                '2 tbsp red wine vinegar 1/2 tsp fresh minced '
                                'rosemary 1/4 teaspoon kosher salt Directions: '
                                'Cook bacon in a large heavy nonstick skillet '
                                'until crispy, about 7 minutes. Transfer to a '
                                'paper towel to drain and set aside. Drain the fat '
                                'but don’t wipe the skillet, leaving any excess '
                                'oil in the pan to cook the chicken. Season '
                                'chicken with salt and rosemary, cook in the '
                                'skillet over medium-high heat until golden and '
                                'cooked through, about 5 minutes on each side. '
                                'Make a bed of the romaine and arugula (or '
                                'watercress) in a large serving bowl or platter '
                                '(or divide between 2 plates). Scatter the cherry '
                                'tomatoes, red onion and bacon on top. Slice the '
                                'avocado, sprinkle with pinch of salt and arrange '
                                'on salad. Slice the chicken thighs and add to the '
                                'salad. To make the rosemary vinaigrette, in a '
                                'small bowl whisk the ingredients. Pour over the '
                                'salad and serve right away. Nutrition Information '
                                'Yield: 2 servings, Serving Size: half of the '
                                'salad Amount Per Serving: Smart Points: 10 Points '
                                '+: 10 Calories: 381 Total Fat: 25g Saturated Fat: '
                                '5g Cholesterol: 114mg Sodium: 741mg '
                                'Carbohydrates: 12g Fiber: 6g Sugar: 1g Protein: '
                                '29g posted April 28, 2016 by Gina Get new free '
                                'recipes and exclusive content delivered right to '
                                'your inbox:'},
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
                                'dairy, soy, nut, shellfish and cane sugar. But '
                                'don’t be fooled, the recipes are amazing and her '
                                'photography is stunning! For this recipe, I '
                                'modified the ingredients slightly to lower the '
                                'calories buy reducing the olive oil a bit, and '
                                'using skinless thighs instead of using the skin. '
                                'If you want to further reduce the calories you '
                                'can use chicken breast instead and use 1/2 of an '
                                'avocado. This recipe was a keeper, also great for '
                                'the summer if you want to make the chicken on the '
                                'grill. Rosemary Chicken Salad with Avocado and '
                                'Bacon This hearty Rosemary Chicken Salad with '
                                'Avocado and Bacon is HUGE – perfect when you want '
                                "a low-carb meal that will fill you up! It's also "
                                'gluten-free, dairy-free, egg-free and soy-free '
                                'for people with food allergies. Ingredients: 3 '
                                'slices center-cut bacon, diced 2 boneless, '
                                'trimmed skinless chicken thighs (4 oz each) 1/2 '
                                'teaspoon kosher salt 1 tbsp fresh rosemary 3 cups '
                                'chopped romaine lettuce, chopped 1/2 cup baby '
                                'arugula or watercress 1/2 cup halved cherry '
                                'tomatoes 3 tablespoons chopped red onion 4 oz '
                                'avocado, sliced (1 small) For the rosemary '
                                'vinaigrette: 1 tsp dijon mustard 4 tsp olive oil '
                                '2 tbsp red wine vinegar 1/2 tsp fresh minced '
                                'rosemary 1/4 teaspoon kosher salt Directions: '
                                'Cook bacon in a large heavy nonstick skillet '
                                'until crispy, about 7 minutes. Transfer to a '
                                'paper towel to drain and set aside. Drain the fat '
                                'but don’t wipe the skillet, leaving any excess '
                                'oil in the pan to cook the chicken. Season '
                                'chicken with salt and rosemary, cook in the '
                                'skillet over medium-high heat until golden and '
                                'cooked through, about 5 minutes on each side. '
                                'Make a bed of the romaine and arugula (or '
                                'watercress) in a large serving bowl or platter '
                                '(or divide between 2 plates). Scatter the cherry '
                                'tomatoes, red onion and bacon on top. Slice the '
                                'avocado, sprinkle with pinch of salt and arrange '
                                'on salad. Slice the chicken thighs and add to the '
                                'salad. To make the rosemary vinaigrette, in a '
                                'small bowl whisk the ingredients. Pour over the '
                                'salad and serve right away. Nutrition Information '
                                'Yield: 2 servings, Serving Size: half of the '
                                'salad Amount Per Serving: Smart Points: 10 Points '
                                '+: 10 Calories: 381 Total Fat: 25g Saturated Fat: '
                                '5g Cholesterol: 114mg Sodium: 741mg '
                                'Carbohydrates: 12g Fiber: 6g Sugar: 1g Protein: '
                                '29g posted April 28, 2016 by Gina Get new free '
                                'recipes and exclusive content delivered right to '
                                'your inbox:'},
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
                                'dairy, soy, nut, shellfish and cane sugar. But '
                                'don’t be fooled, the recipes are amazing and her '
                                'photography is stunning! For this recipe, I '
                                'modified the ingredients slightly to lower the '
                                'calories buy reducing the olive oil a bit, and '
                                'using skinless thighs instead of using the skin. '
                                'If you want to further reduce the calories you '
                                'can use chicken breast instead and use 1/2 of an '
                                'avocado. This recipe was a keeper, also great for '
                                'the summer if you want to make the chicken on the '
                                'grill. Rosemary Chicken Salad with Avocado and '
                                'Bacon This hearty Rosemary Chicken Salad with '
                                'Avocado and Bacon is HUGE – perfect when you want '
                                "a low-carb meal that will fill you up! It's also "
                                'gluten-free, dairy-free, egg-free and soy-free '
                                'for people with food allergies. Ingredients: 3 '
                                'slices center-cut bacon, diced 2 boneless, '
                                'trimmed skinless chicken thighs (4 oz each) 1/2 '
                                'teaspoon kosher salt 1 tbsp fresh rosemary 3 cups '
                                'chopped romaine lettuce, chopped 1/2 cup baby '
                                'arugula or watercress 1/2 cup halved cherry '
                                'tomatoes 3 tablespoons chopped red onion 4 oz '
                                'avocado, sliced (1 small) For the rosemary '
                                'vinaigrette: 1 tsp dijon mustard 4 tsp olive oil '
                                '2 tbsp red wine vinegar 1/2 tsp fresh minced '
                                'rosemary 1/4 teaspoon kosher salt Directions: '
                                'Cook bacon in a large heavy nonstick skillet '
                                'until crispy, about 7 minutes. Transfer to a '
                                'paper towel to drain and set aside. Drain the fat '
                                'but don’t wipe the skillet, leaving any excess '
                                'oil in the pan to cook the chicken. Season '
                                'chicken with salt and rosemary, cook in the '
                                'skillet over medium-high heat until golden and '
                                'cooked through, about 5 minutes on each side. '
                                'Make a bed of the romaine and arugula (or '
                                'watercress) in a large serving bowl or platter '
                                '(or divide between 2 plates). Scatter the cherry '
                                'tomatoes, red onion and bacon on top. Slice the '
                                'avocado, sprinkle with pinch of salt and arrange '
                                'on salad. Slice the chicken thighs and add to the '
                                'salad. To make the rosemary vinaigrette, in a '
                                'small bowl whisk the ingredients. Pour over the '
                                'salad and serve right away. Nutrition Information '
                                'Yield: 2 servings, Serving Size: half of the '
                                'salad Amount Per Serving: Smart Points: 10 Points '
                                '+: 10 Calories: 381 Total Fat: 25g Saturated Fat: '
                                '5g Cholesterol: 114mg Sodium: 741mg '
                                'Carbohydrates: 12g Fiber: 6g Sugar: 1g Protein: '
                                '29g posted April 28, 2016 by Gina Get new free '
                                'recipes and exclusive content delivered right to '
                                'your inbox:'},
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
 
