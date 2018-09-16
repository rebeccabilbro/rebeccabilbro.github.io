---
layout: post
title:  SPARQL Queries for Local RDF Data
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-07-05 19:32
---

So you found some RDF data (yay!) from an archive somewhere, but there's no active SPARQL endpoint (it's all JSON APIs these days). You could use the methods implemented in the Python package `rdflib` to perform some lightweight searches of the triples, but what if you want to perform more complex queries without having to create a local triple store? In this post we'll see how to use the declarative language of SPARQL to perform complex queries on a local RDF file (inspired by [this Stackoverflow post](https://stackoverflow.com/questions/9877989/python-sparql-querying-local-file)).

_Note: If you want to follow along at home, check out the post on [RDF basics](https://rebeccabilbro.github.io/rdf-basics/) to find out how to get the [data](http://data.dws.informatik.uni-mannheim.de/structureddata/2014-12/quads/ClassSpecificQuads/schemaorgProduct.nq.sample.txt) used in this post, where it comes from, and what it's all about._

## Make a `ConjunctiveGraph`

First, make sure you have `pip` installed `rdflib`. Now make a `ConjunctiveGraph` from the data. Here we specify that the data should be parsed as nquads, since that's the form that this specific dataset takes.


```python
import os

from rdflib import ConjunctiveGraph

base_folder = "data"
product_path = "products.nq"


def make_graph_from_nquads(input_data):
    g = ConjunctiveGraph(identifier="Products")
    data = open(input_data, "rb")
    g.parse(data, format="nquads")

    return g

g = make_graph_from_nquads(os.path.join(base_folder, product_path))
```

## Query the `rdflib.graph.Graph()`

Now that we have a graph, `rdflib` exposes a `Graph.query` module that we can use to pass in SPARQL queries.

Let's create a reusable function `get_products`, that takes as an argument the `ConjunctiveGraph` and returns a list of products.


```python
from rdflib import URIRef, BNode

def get_products(graph):

    product = URIRef("http://schema.org/Product")

    sparql_query = """
        SELECT DISTINCT ?s
        WHERE {
        ?s ?p ?o .
        }
        """

    results = graph.query(sparql_query, initBindings={'o' : product})
    return [str(result[0]) for result in results]
```

Now we can use our function to get all the unique products in the dataset:


```python
products = get_products(g)

print("{} total products".format(len(products)))
print("URI of first product: {}".format(list(products)[0]))
```

    216 total products
    URI of first product: Neaca176676eb429cb27c9aff6ef60886


Now let's create a function `get_product_details` that takes as input the graph and a specific product's uri, and returns all the results containing the details available for that product:


```python
def get_product_details(graph, product_uri):

    sparql_query = """
    SELECT ?p ?o
    WHERE {
    ?s ?p ?o .
    }
    """

    return graph.query(sparql_query, initBindings={'s' : product_uri})
```

We can test out our function to explore a specific product from our dataset (in this case the one corresponding to the anonymous node 'N5ff6dab3a3ec40b4a040220b8f2effbe'):


```python
sample_product = BNode('N5ff6dab3a3ec40b4a040220b8f2effbe')
details = get_product_details(g, sample_product)
for detail in details:
    print(detail,'\n')
```

This tells that the product has some additional information, including a name ("sandcastle1"), a description ("Check out sandcastle1 on Cubify at http://cubify.com/Store/Design/AL98QAW7QL #getthereeasy"), and an image:

![sandcastle1 image](http://cubify.blob.core.windows.net/account/QHUHU2JGQ9/GOUAOFHO5W/cb863880-2a9e-457b-ae6d-574d9b46e49f_e719dda8-c96b-4242-bccb-bfa5c28e061c_08fb68af-884d-4b5f-89f3-89)

We can use the same function to get the details for every product in the dataset:


```python
for product in products:
    print(product,':')
    for detail in get_product_details(g, BNode(product)):
        print('- ', detail)
    print('')
```

    N2959f8145c2247d894f354fb3a142412 :
    -  (rdflib.term.URIRef('http://schema.org/Product/description'), rdflib.term.Literal('In Your Face Apparel Junior Ref Tank is made of 92/8 microfiber poly-spandex.  This is not an official referee jersey.', lang='en'))
    -  (rdflib.term.URIRef('http://schema.org/Product/name'), rdflib.term.Literal('\n\t\tIn Your Face Apparel Junior Ref Tank\n\t', lang='en'))
    -  (rdflib.term.URIRef('http://schema.org/Product/brand'), rdflib.term.Literal('In Your Face Apparel', lang='en'))
    -  (rdflib.term.URIRef('http://schema.org/Product/image'), rdflib.term.URIRef('http://epicsports.cachefly.net/images/37096/300/in-your-face-apparel-junior-ref-tank.jpg'))
    -  (rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://schema.org/Product')

    N217811699c844dea9dd2a36488277cec :
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('Nebda98b0b3d640e39f79a04d91352e64'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N71ee1fb4a62d415cb6d8090c86642a37'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('Na306cd3a72c746c58ea8f5b923bc2af5'))
    -  (rdflib.term.URIRef('http://schema.org/Product/name'), rdflib.term.Literal('Epson Stylus SX515W', lang='en-us'))
    -  (rdflib.term.URIRef('http://schema.org/Product/image'), rdflib.term.URIRef('http://ii.alatest.com/product/190x190/6/5/Epson-Stylus-SX515W-High-Speed-All-in-One-Printer-with-Individual-Inks-and-Wi-Fi-0.jpg'))
    -  (rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://schema.org/Product'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('Nd1754af480da4bb5a0799fa49cf552f4'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N267b5ee1d8374709857ef585427dbeaa'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N4bc618e5e20c4124b4c8ffe48990d4bb'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N932c11c11c3b49d6ac61f896698b9ace'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N5e9fab20825e4bf9a7e7d852d58b0a54'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N22d14f219ae74122802e4dd18ca3e0dd'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N8752f2883bf34f4ca8ad6716416392a3'))
    -  (rdflib.term.URIRef('http://schema.org/Product/review'), rdflib.term.BNode('N7c30e4a53af44456a0d01f2aded42212'))

  ...


Now let's say we want to go through each product and find not only the information contained in it's primary triples, but also information in related triples, such as the product reviews, which are stored separately, and of which there may be several or none for a given product.

```python
generic = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
review_desc = URIRef('http://schema.org/Review/description')
product_review = URIRef('http://schema.org/Product/review')   


def get_review(graph, review_uri):

    sparql_query = """
    SELECT ?p ?o
    WHERE {
    ?s ?p ?o .
    }
    """

    return graph.query(sparql_query, initBindings={'s': review_uri})


# make a dictionary to hold all of the product data
product_dict = {}

for product in products:
    product_dict[product] = {"http://schema.org/Product/name" : None,
                             "http://schema.org/Product/image": None,
                             "http://schema.org/Product/url" :  None,
                             "http://schema.org/Product/description": None,
                             "http://schema.org/Product/sku" : None,
                             "http://schema.org/Product/manufacturer": None,
                             "http://schema.org/Product/productID": None,
                             "http://schema.org/Product/dateModified": None,
                             "http://schema.org/Product/releaseDate": None,
                             "http://schema.org/Product/brand": None,
                             "http://schema.org/Product/model": None,
                             "http://schema.org/Product/offers": None,
                             "http://schema.org/Product/thumbnailUrl": None,
                             "http://schema.org/Product/logo": None,
                             "http://schema.org/Product/aggregateRating": None,
                             "http://schema.org/Product/reviews": [],
        }
    for detail_type, detail_content in get_product_details(g, BNode(product)):
        if detail_type == generic:
            continue
        # if the details indicate a product review:
        elif detail_type == product_review:
            for review_type, review_content in get_review(g, detail_content):
                if review_type == review_desc:
                    product_dict[product]["http://schema.org/Product/reviews"].append(
                        str(review_content)
                    )
                else:
                    continue
        else:
            product_dict[product][detail_type] = str(detail_content)
```


```python
product_dict
```


     {'N326f7a36c7ac4bb2bcda3d21ad65c11a': {
          'http://schema.org/Product/name': None,
          'http://schema.org/Product/image': None,
          'http://schema.org/Product/url': None,
          'http://schema.org/Product/description': None,
          'http://schema.org/Product/sku': None,
          'http://schema.org/Product/manufacturer': None,
          'http://schema.org/Product/productID': None,
          'http://schema.org/Product/dateModified': None,
          'http://schema.org/Product/releaseDate': None,
          'http://schema.org/Product/brand': None,
          'http://schema.org/Product/model': None,
          'http://schema.org/Product/offers': None,
          'http://schema.org/Product/thumbnailUrl': None,
          'http://schema.org/Product/logo': None,
          'http://schema.org/Product/aggregateRating': None,
          'http://schema.org/Product/reviews': [
              'alaTest has collected and analyzed 40 user reviews of HVTS18DABB Black 18 Bottle Freestanding Wine Refrigerator from Amazon.com. The average user rating for this product is 1.1/5, compared to an average user rating of 3.7/5 for other Fridges & Freezers on Amazon.com.',
              'This is a piece of junk. Spend a bit more and buy a better quality product',
              'Haier has obviously designed this product to have a useful life of 13 months which is why they set the warranty period at 12 months. Do not buy this product unless you enjoy throwing money away.'],
              },

        ...

      }

Success! Now we have a dictionary representation of all of our products, together with their reviews.
